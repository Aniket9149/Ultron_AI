"""
skills/game_engine_architect/editor_automator.py
Procedural scene generation via Unity Editor menu item.
"""
from pathlib import Path

TERRAIN_AUTOMATION_CS = """using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;

namespace UltronStudio.EditorTools
{
    public static class TerrainAutomator
    {
        [MenuItem("Ultron/Generate Survival Scene")]
        public static void GenerateSurvivalScene()
        {
            Debug.Log("[Ultron Studio] Building procedural survival biome...");

            // 1. Terrain Data
            TerrainData tData = new TerrainData();
            tData.heightmapResolution = 513;
            tData.size = new Vector3(600, 100, 600);

            int res = tData.heightmapResolution;
            float[,] heights = new float[res, res];
            float scale = 0.012f;

            for (int x = 0; x < res; x++)
            {
                for (int y = 0; y < res; y++)
                {
                    heights[x, y] = Mathf.PerlinNoise(x * scale, y * scale) * 0.2f;
                }
            }
            tData.SetHeights(0, 0, heights);

            GameObject terrainObj = Terrain.CreateTerrainGameObject(tData);
            terrainObj.name = "SurvivalTerrain";
            terrainObj.transform.position = Vector3.zero;

            // 2. Directional Sun
            GameObject sun = GameObject.Find("Directional Light");
            if (sun == null)
            {
                sun = new GameObject("Directional Light");
                Light l = sun.AddComponent<Light>();
                l.type = LightType.Directional;
            }
            sun.transform.rotation = Quaternion.Euler(45f, -30f, 0f);

            // 3. Player Spawn Marker
            GameObject player = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            player.name = "Player_Spawn";
            player.transform.position = new Vector3(250, 30, 250);

            EditorSceneManager.MarkAllScenesDirty();
            Debug.Log("[Ultron Studio] Scene constructed successfully!");
        }
    }
}
"""

def inject_terrain_automator(project_path: Path):
    editor_dir = project_path / "Assets" / "Editor"
    editor_dir.mkdir(parents=True, exist_ok=True)
    script_file = editor_dir / "TerrainAutomator.cs"
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(TERRAIN_AUTOMATION_CS)
