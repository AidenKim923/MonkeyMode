using System;
using System.IO;
using UnityEditor;
using UnityEditor.Build.Reporting;

namespace <AssemblyPrefix>Editor.Automation
{
    public static class AgentBuild
    {
        private const string OutputArgument = "-agentBuildOutput";
        private const string ExecutableName = "<YourGame>.exe";

        public static void Build()
        {
            string outputDirectory = ReadArgument(OutputArgument);
            string[] scenes = EnabledScenePaths();
            if (scenes.Length == 0)
            {
                Fail("No enabled scenes in Build Settings. Add your bootstrap scene to Build Settings.");
            }

            var options = new BuildPlayerOptions
            {
                scenes = scenes,
                locationPathName = Path.Combine(outputDirectory, ExecutableName),
                target = EditorUserBuildSettings.activeBuildTarget,
                options = BuildOptions.Development | BuildOptions.StrictMode,
            };

            BuildReport report = BuildPipeline.BuildPlayer(options);
            if (report.summary.result != BuildResult.Succeeded)
            {
                Fail($"Build failed: {report.summary.result}, {report.summary.totalErrors} error(s)");
            }

            EditorApplication.Exit(0);
        }

        private static string[] EnabledScenePaths()
        {
            var paths = new System.Collections.Generic.List<string>();
            foreach (EditorBuildSettingsScene scene in EditorBuildSettings.scenes)
            {
                if (scene.enabled)
                {
                    paths.Add(scene.path);
                }
            }
            return paths.ToArray();
        }

        private static string ReadArgument(string name)
        {
            string[] args = Environment.GetCommandLineArgs();
            for (int i = 0; i < args.Length - 1; i++)
            {
                if (args[i] == name)
                {
                    return args[i + 1];
                }
            }
            Fail($"Required argument {name} is missing. Run this through tools/Invoke-UnityBuild.ps1.");
            return null;
        }

        private static void Fail(string message)
        {
            UnityEngine.Debug.LogError(message);
            EditorApplication.Exit(1);
        }
    }
}
