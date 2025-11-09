# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class GitfilesPlugin(
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin
):

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(url="https://github.com/YourUserID/YourRepository.git", path="gitfiles")

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/gitfiles.js"],
            "css": ["css/gitfiles.css"],
            "less": ["less/gitfiles.less"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/main/bundledplugins/softwareupdate.html
        # for details.
        return {
            "gitfiles": {
                "displayName": "Gitfiles Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "mhughes2k",
                "repo": "OctoPrint-Gitfiles",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/mhughes2k/OctoPrint-Gitfiles/archive/{target_version}.zip",
            }
        }
    # SimpleAPIPlugin mixin
    def get_api_commands(self):
        return dict(
            git=["arg1"]
        )
    def on_api_command(self, command, data):
        import flask
        if command == "git":
            if self._settings.get(["url"]) == "https://github.com/YourUserID/YourRepository.git":
                self._logger.info("Problem with setup. Please visit Settings -> GitFiles and adjust the URL")
                return

            uploads = self._settings.global_get_basefolder("uploads")
            path =    self._settings.get(["path"])
            url =     self._settings.get(["url"])
            verb =    "{arg1}".format(**data)
            
            if path == "" or path == "uploads":
                gitfilesFolder = uploads
            else:
                gitfilesFolder = uploads + "/" + path
            self._logger.info("Path: `{}`".format(gitfilesFolder))
            # In the indicated path, issue a `git remote get-url origin` to determine whether
            # or not it's been initialized before
            try:
                self._logger.info("Testing the indicated `{}` folder...".format(gitfilesFolder))
                output =  call(["git", "remote", "get-url", "origin"], cwd=gitfilesFolder)
                if output > 0:
                    self.init(output, gitfilesFolder, url)
            except OSError as e:
                self._logger.info("Indicated folder is not initialized yet, throwing error")
                output = "N/A"
                self.init(output, gitfilesFolder, url)

            # This one runs regardless of whether or not it's been previously initialized
            try:
                self._logger.info("-- git {} origin master ---------------------------------------------------".format(verb))
                output =  call(["git", verb, "origin", "master"], cwd=gitfilesFolder)
                self._logger.info("git returned: " + str(output))
                self._logger.info("-- (end of git {}) --------------------------------------------------------".format(verb))
            except OSError as e:
                self._logger.info("`git {}` failed".format(verb))
    
    # This is called when an API command is issued to make sure
    # that everything is actually working / set up correctly.
    # It's not the plugin itself's initialization.
    def init(self, output, gitfilesFolder, url):
        self._logger.info("Path is not initialized already, returned error: `{}`".format(output))
        # TODO: Test to see if the output is the correct remote
        if not os.path.isdir(gitfilesFolder):
            try:
                self._logger.info("Creating the new `{}` subfolder...".format(gitfilesFolder))
                os.mkdir(gitfilesFolder, 0o755)
                self._logger.info("Created")
            except OSError as e:
                self._logger.info("Subfolder creation failed")
                return
        try:
            self._logger.info("Initializing...")
            output =  call(["git", "init"], cwd=gitfilesFolder)
            self._logger.info(output)
        except OSError as e:
            self._logger.info("`git init` failed")
            return
        try:
            self._logger.info("Setting up the remote origin for master...")
            output =  call(["git", "remote", "add", "origin", url], cwd=gitfilesFolder)
            self._logger.info(output)
        except OSError as e:
            self._logger.info("`git add remote origin` failed")
            return


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Gitfiles Plugin"

__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

__plugin_implementation__ = GitfilesPlugin()


__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}
