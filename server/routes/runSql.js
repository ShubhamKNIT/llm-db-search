import express from "express";
const router = express.Router();

import pool from "../db/pool.js";
import isSafeSql from "../utils/validateSql.js";

router.post("/run-sql", async (req, res) => {
  const { sql } = req.body;

  if (!sql || typeof sql !== "string") {
    return res.status(400).json({ error: "Missing or invalid SQL." });
  }

  try {
    // Split SQL into multiple queries
    const queries = sql
      .split(";")
      .map(q => q.trim())
      .filter(q => q.length > 0);

    const allResults = [];

    for (const query of queries) {
      if (!isSafeSql(query)) {
        return res.status(400).json({ error: `Unsafe or disallowed SQL query: ${query}` });
      }

      const result = await pool.query(query);
      allResults.push({ query, rows: result.rows });
    }

    res.json({ results: allResults });

  } catch (err) {
    console.error("SQL Execution Error:", err);
    res.status(500).json({ error: "Query execution failed.", detail: err.message });
  }
});

export default router;
