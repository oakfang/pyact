import * as mui from "@mui/material";
import * as icons from "@mui/icons-material";
import * as rooks from "rooks";
import "./index.css";
import { install } from "./pyact";

async function main() {
  const pyodide = await install();
  await pyodide.loadPackage("pillow");
  pyodide.registerJsModule("mui", mui);
  pyodide.registerJsModule("icons", icons);
  pyodide.registerJsModule("rooks", rooks);

  await pyodide.runPythonAsync(`
    import micropip
    await micropip.install("/lib/app/dist/app-0.0.1-py3-none-any.whl")
    from app import main
    main()
  `);
}

main();
