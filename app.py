import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";
import { z } from "zod";

const app = express();
app.use(express.json());

const GOOGLE_SCRIPT_URL =
  "https://script.google.com/macros/s/AKfycbyEN2rj_WGPKqzew0GuJbogrS4BWt1OPfVfZTIdl7rIUCI7cJS2CZh8sIuC1vH7Smc96w/exec";

function createServer() {
  const server = new McpServer({
    name: "college-ai-mcp",
    version: "1.0.0"
  });

  server.tool(
    "college_search",
    "ค้นหาข้อมูลของวิทยาลัยเทคนิคจุฬาภรณ์ (ลาดขวาง) จากฐานข้อมูล Google Sheets",
    {
      keyword: z.string().describe("คำค้นหาที่ต้องการค้น เช่น ช่างไฟฟ้า สมัครเรียน ค่าเทอม")
    },
    async ({ keyword }) => {
      try {
        const response = await fetch(
          ${GOOGLE_SCRIPT_URL}?q=${encodeURIComponent(keyword)}
        );

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
              text: เกิดข้อผิดพลาดในการค้นข้อมูล: ${error.message}
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

app.all("/mcp", async (req, res) => {
  const server = createServer();

  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined
  });

  res.on("close", async () => {
    await transport.close();
    await server.close();
  });

  await server.connect(transport);
  await transport.handleRequest(req, res);
});

const PORT = process.env.PORT || 10000;

app.listen(PORT, "0.0.0.0", () => {
  console.log(`College AI MCP Server running on port ${PORT}`);
});
