const express = require("express");
const sql = require("mssql");
const cors = require("cors");

const app = express();
app.use(cors());

const config = {
  user: "MasterLog",
  password: "Master1252@#",
  server: "sistema.atdata.com.br",
  port: 35987,
  options: {
    encrypt: false,
    trustServerCertificate: true
  }
};

async function consultar(cdprop) {
  try {
    await sql.connect(config);

    const result = await sql.query(`
      SELECT 
        cdmaterialestoque,
        dsmaterialservico,
        SUM(qtENTRADA) AS ENTRADA,
        SUM(qtdesaldo) AS SALDO
      FROM vwr_posicaoestoque
      WHERE cdpropestoque = ${cdprop}
      GROUP BY cdmaterialestoque, dsmaterialservico
      ORDER BY cdmaterialestoque
    `);

    return result.recordset;
  } catch (err) {
    throw err;
  }
}

app.get("/gestor/:codigo", async (req, res) => {
  try {
    const data = await consultar(req.params.codigo);
    res.json(data);
  } catch (err) {
    res.status(500).json({ erro: err.message });
  }
});

app.get("/", (req, res) => {
  res.json({ status: "API rodando" });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log("Servidor rodando na porta " + PORT);
});
