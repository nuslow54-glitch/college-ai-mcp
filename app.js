import express from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const app = express();

app.use(express.json());

const GOOGLE_SCRIPT_URL =
  "https://script.google.com/macros/s/AKfycbyEN2rj_WGPKqzew0GuJbogrS4BWt1OPfVfZTIdl7rIUCI7cJS2CZh8sIuC1vH7Smc96w/exec";

function createMcpServer() {
  const server = new McpServer({
    name: "college-ai-mcp",
    version: "1.0.0"
  });

  server.tool(
    "college_search",
    "ค้นหาข้อมูลวิทยาลัยเทคนิคจุฬาภรณ์ (ลาดขวาง)",
    {
      keyword: z.string()
    },
    async ({ keyword }) => {
      try {
        const url =
          GOOGLE_SCRIPT_URL +
          "?q=" +
          encodeURIComponent(keyword);

        const response = await fetch(url);
        const data = await response.json();

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(data.results || [], null, 2)
            }
          ]
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: "ไม่สามารถค้นข้อมูลวิทยาลัยได้: " + error.message
            }
          ],
          isError: true
        };
      }
    }
  );

  return server;
}

app.get("/", (req, res) => {
  res.send("College AI MCP Server is running");
});

app.post("/mcp", async (req, res) => {
  const server = createMcpServer();

  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
    enableJsonResponse: true
  });

  try {
    await server.connect(transport);

    await transport.handleRequest(req, res, req.body);
  } catch (error) {
    console.error(error);

    if (!res.headersSent) {
      res.status(500).json({
        error: error.message
      });
    }
  }
});

const PORT = process.env.PORT || 10000;

app.listen(PORT, "0.0.0.0", () => {
  console.log(`College AI MCP Server running on port ${PORT}`);
});
