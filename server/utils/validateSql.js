// server/utils/validateSql.js

const ALLOWED_TABLES = ["mobiles", "laptops"];
const BANNED_KEYWORDS = [";", "--", "drop", "delete", "update", "insert", "alter", "truncate"];

function isSafeSql(sql) {
  const lowered = sql.trim().toLowerCase();
  if (!lowered.startsWith("select")) return false;
  if (BANNED_KEYWORDS.some(kw => lowered.includes(kw))) return false;
  if (!ALLOWED_TABLES.some(table => lowered.includes(`from ${table}`))) return false;
  return true;
}

export default isSafeSql;
