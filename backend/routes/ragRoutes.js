const express = require("express");
const router = express.Router();
const axios = require("axios");

// RAG Agents API URL (FastAPI server)
const RAG_API_URL = process.env.RAG_API_URL || "http://localhost:8000";

/**
 * @route   POST /api/rag/query
 * @desc    Forward query to RAG agents and get drug repurposing insights
 * @access  Public (add auth middleware if needed)
 */
router.post("/query", async (req, res) => {
    try {
        const { query, output_format = "text", include_charts = true, include_tables = true, generate_report = false } = req.body;

        if (!query || query.trim() === "") {
            return res.status(400).json({
                success: false,
                error: "Query is required"
            });
        }

        console.log(`📝 Received query: ${query}`);

        // Forward request to RAG agents FastAPI server
        const response = await axios.post(`${RAG_API_URL}/api/query`, {
            query,
            output_format,
            include_charts,
            include_tables,
            generate_report
        }, {
            timeout: 300000, // 5 minute timeout for complex queries
            headers: {
                "Content-Type": "application/json"
            }
        });

        console.log(`✅ RAG agents responded successfully`);

        res.json(response.data);

    } catch (error) {
        console.error("❌ RAG query error:", error.message);

        if (error.response) {
            // RAG API responded with an error
            return res.status(error.response.status).json({
                success: false,
                error: error.response.data?.detail || "RAG agents error",
                message: error.message
            });
        } else if (error.code === "ECONNREFUSED") {
            // RAG API server is not running
            return res.status(503).json({
                success: false,
                error: "RAG agents service is unavailable. Please ensure the Python FastAPI server is running.",
                message: "Connection refused to RAG API server"
            });
        } else {
            return res.status(500).json({
                success: false,
                error: "Internal server error",
                message: error.message
            });
        }
    }
});

/**
 * @route   GET /api/rag/health
 * @desc    Check health of RAG agents service
 * @access  Public
 */
router.get("/health", async (req, res) => {
    try {
        const response = await axios.get(`${RAG_API_URL}/api/health`, {
            timeout: 5000
        });
        res.json({
            success: true,
            ragAgents: response.data
        });
    } catch (error) {
        res.status(503).json({
            success: false,
            error: "RAG agents service is unavailable",
            message: error.message
        });
    }
});

/**
 * @route   GET /api/rag/agents
 * @desc    Get list of available agents and their capabilities
 * @access  Public
 */
router.get("/agents", async (req, res) => {
    try {
        const response = await axios.get(`${RAG_API_URL}/api/agents`, {
            timeout: 10000
        });
        res.json({
            success: true,
            agents: response.data
        });
    } catch (error) {
        console.error("Error fetching agents:", error.message);
        res.status(503).json({
            success: false,
            error: "Failed to fetch agents information"
        });
    }
});

/**
 * @route   GET /api/rag/examples
 * @desc    Get example queries
 * @access  Public
 */
router.get("/examples", async (req, res) => {
    try {
        const response = await axios.get(`${RAG_API_URL}/api/examples`, {
            timeout: 5000
        });
        res.json(response.data);
    } catch (error) {
        // Return default examples if RAG API is unavailable
        res.json({
            examples: [
                {
                    query: "Analyze the market potential for Metformin in oncology indications",
                    description: "Market analysis for drug repurposing"
                },
                {
                    query: "What is the patent landscape for Pembrolizumab?",
                    description: "Patent and IP analysis"
                },
                {
                    query: "Show me active clinical trials for Rituximab in autoimmune diseases",
                    description: "Clinical trials search"
                },
                {
                    query: "Comprehensive analysis of drug repurposing opportunities in neurology",
                    description: "Multi-agent comprehensive analysis"
                }
            ]
        });
    }
});

module.exports = router;
