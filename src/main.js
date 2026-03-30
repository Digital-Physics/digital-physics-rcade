// import "./style.css";
// import { loadPyodide } from "pyodide";
// import { PLAYER_1, PLAYER_2, SYSTEM } from "@rcade/plugin-input-classic";
// import gameCode from "./game.py?raw";
// import wheels from "virtual:pyodide-wheels";

// async function main() {
//     const pyodide = await loadPyodide({
//         indexURL: "/assets",
//     });

//     // Set up SDL2 canvas for pygame rendering
//     const canvas = document.getElementById("canvas");
//     pyodide.canvas.setCanvas2D(canvas);

//     // Load micropip for installing local wheels
//     await pyodide.loadPackage("micropip");
//     const micropip = pyodide.pyimport("micropip");

//     pyodide.FS.mkdirTree("/src");

//     const modules = import.meta.glob("./*.py", { eager: true, query: "?raw", import: "default" });
//     for (const [path, code] of Object.entries(modules)) {
//         const filename = path.replace("./", "");
//         pyodide.FS.writeFile(`/src/${filename}`, code);
//     }

//     // Add /src to Python's module search path
//     pyodide.runPython(`
//     import sys
//     sys.path.insert(0, "/src")
//     `);

//     // Install all wheels from local assets
//     for (const wheel of wheels) {
//         await micropip.install(`/assets/${wheel}`);
//     }

//     // Create input bridge - called from Python
//     const getInput = () => ({
//         p1: {
//             up: PLAYER_1.DPAD.up,
//             down: PLAYER_1.DPAD.down,
//             left: PLAYER_1.DPAD.left,
//             right: PLAYER_1.DPAD.right,
//             a: PLAYER_1.A,
//             b: PLAYER_1.B,
//         },
//         p2: {
//             up: PLAYER_2.DPAD.up,
//             down: PLAYER_2.DPAD.down,
//             left: PLAYER_2.DPAD.left,
//             right: PLAYER_2.DPAD.right,
//             a: PLAYER_2.A,
//             b: PLAYER_2.B,
//         },
//         system: {
//             start_1p: SYSTEM.ONE_PLAYER,
//             start_2p: SYSTEM.TWO_PLAYER,
//         },
//     });

//     pyodide.globals.set("_get_input", getInput);

//     globalThis.BASE_URL = window.location.origin + "/";

//     // Run the game
//     await pyodide.runPythonAsync(gameCode);
// }

// main();
import "./style.css";
import { loadPyodide } from "pyodide";
import { PLAYER_1, PLAYER_2, SYSTEM } from "@rcade/plugin-input-classic";
import gameCode from "./game.py?raw";
import wheels from "virtual:pyodide-wheels";

function showProgress(message, percent) {
    const el = document.getElementById("loading-text");
    if (el) el.textContent = `${message} (${Math.round(percent)}%)`;
}

async function prefetchAssets(pyodide) {
    const essential = import.meta.glob(
        [
            "../public/audio/**/*",
            "../public/fonts/**/*",
            "../public/levels/**/*",
            "../public/img/**/*",
        ],
        { eager: true, as: "url" }
    );

    const entries = Object.entries(essential).filter(([path]) =>
        // !path.includes("movie_png_seq") &&
        // !path.includes("img/transition") &&
        // !path.includes("nca_room_movie") &&
        !path.includes(".DS_Store")
    );

    const BASE_FS = "/home/pyodide";
    console.log("Fetching", entries.length, "essential assets...");
    let done = 0;

    for (const [globKey, _] of entries) {
        const relativePath = globKey.replace(/^\.\.\/public\//, "");
        const serverPath = "/" + relativePath;
        const fsPath = `${BASE_FS}/${relativePath}`;

        try {
            const response = await fetch(serverPath);
            if (response.status >= 400) {
                console.warn(`Failed to fetch ${serverPath}: ${response.status}`);
                continue;
            }
            const buffer = await response.arrayBuffer();
            const data = new Uint8Array(buffer);

            const dir = fsPath.substring(0, fsPath.lastIndexOf("/"));
            pyodide.FS.mkdirTree(dir);
            pyodide.FS.writeFile(fsPath, data);

            done++;
            showProgress("Loading assets", (done / entries.length) * 100);
        } catch (err) {
            console.error(`Failed on: ${fsPath}`, err);
            throw err;
        }
    }
    console.log("Assets loaded:", done);
}

async function main() {
    try {
        showProgress("Starting Pyodide", 0);
        const pyodide = await loadPyodide({ indexURL: "/assets" });
        console.log("✓ Pyodide loaded");

        const canvas = document.getElementById("canvas");
        pyodide.canvas.setCanvas2D(canvas);

        // Make canvas focusable and grab focus on click
        canvas.setAttribute("tabindex", "0");
        canvas.style.outline = "none";
        canvas.addEventListener("click", () => canvas.focus());
        canvas.focus();
        console.log("✓ Canvas set");

        showProgress("Installing packages", 0);
        await pyodide.loadPackage("micropip");
        const micropip = pyodide.pyimport("micropip");
        for (const wheel of wheels) {
            await micropip.install(`/assets/${wheel}`);
        }
        console.log("✓ Wheels installed");

        pyodide.FS.mkdirTree("/src");
        const modules = import.meta.glob("./*.py", { eager: true, query: "?raw", import: "default" });
        for (const [path, code] of Object.entries(modules)) {
            const filename = path.replace("./", "");
            pyodide.FS.writeFile(`/src/${filename}`, code);
        }
        pyodide.runPython(`import sys; sys.path.insert(0, "/src")`);
        console.log("✓ Python modules mounted");

        await prefetchAssets(pyodide);
        console.log("✓ Assets prefetched");

        // Debug: verify a known file exists
        pyodide.runPython(`
        import os
        print("audio dir contents:", os.listdir("audio"))
        `);

        globalThis.fetchFileIntoFS = async (relativePath) => {
            const url = "/" + relativePath;
            const response = await fetch(url);
            if (response.status >= 400) throw new Error(`404: ${url}`);
            const buffer = await response.arrayBuffer();
            const data = new Uint8Array(buffer);
            const fsPath = `/home/pyodide/${relativePath}`;
            const dir = fsPath.substring(0, fsPath.lastIndexOf("/"));
            pyodide.FS.mkdirTree(dir);
            pyodide.FS.writeFile(fsPath, data);
        };

        const getInput = () => ({
            p1: {
                up: PLAYER_1.DPAD.up,
                down: PLAYER_1.DPAD.down,
                left: PLAYER_1.DPAD.left,
                right: PLAYER_1.DPAD.right,
                a: PLAYER_1.A,
                b: PLAYER_1.B,
            },
            p2: {
                up: PLAYER_2.DPAD.up,
                down: PLAYER_2.DPAD.down,
                left: PLAYER_2.DPAD.left,
                right: PLAYER_2.DPAD.right,
                a: PLAYER_2.A,
                b: PLAYER_2.B,
            },
            system: {
                start_1p: SYSTEM.ONE_PLAYER,
                start_2p: SYSTEM.TWO_PLAYER,
            },
        });
        pyodide.globals.set("_get_input", getInput);
        console.log("✓ Input bridge set");

        const loadingEl = document.getElementById("loading-text");
        if (loadingEl) loadingEl.style.display = "none";

        console.log("✓ Starting game...");
        await pyodide.runPythonAsync(gameCode);

    } catch (err) {
        console.error("FAILED AT:", err);
        console.error(err.stack);
    }
}

main();