import React from "react";
import ReactDOM from "react-dom/client";

export async function install() {
  const pyodideScript = document.createElement("script");
  pyodideScript.src =
    "https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js";
  document.head.appendChild(pyodideScript);
  await new Promise((resolve) => (pyodideScript.onload = resolve));
  const pyodide = await window.loadPyodide();
  await pyodide.loadPackage("micropip");
  pyodide.registerJsModule("react", React);
  pyodide.registerJsModule("react_dom", ReactDOM);

  await pyodide.runPythonAsync(`
      import micropip
      await micropip.install("/lib/pyact/dist/pyact-0.0.1-py3-none-any.whl")
    `);

  return pyodide;
}
