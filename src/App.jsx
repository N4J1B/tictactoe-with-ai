import { useEffect, useState } from 'react';
import './App.css';
import Square from './kotak.jsx'
import { findBestMove, cekPemenang } from './algoritma.jsx';

export default function App() {
  const [histori, setHistori] = useState([Array(9).fill(null)]);
  const [move, setMove] = useState(0);
  const [isi, setIsi] = useState(Array(9).fill(null));
  const giliranX = move % 2 === 0;
  const [giliranAI, setGiliranAI] = useState('O');
  const [jenisAI, setJenisAI] = useState("Minimax")

  const handleClick = (i) => {
    if (isi[i] || cekPemenang(isi)) return;
    const isiBaru = isi.slice();
    isiBaru[i] = giliranX ? "X" : "O";
    const historiBaru = [...histori, isiBaru];
    setHistori(historiBaru);
    setIsi(isiBaru);
    setMove(historiBaru.length - 1);
  };

  function getAIRL(board, AI) {
    board = board.map((val) => (val === 'X' ? 1 : val === 'O' ? -1 : 0));
    fetch(`${import.meta.env.VITE_BACKEND_URL}/predict_move`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ board: board, player_turn: AI === 'X' ? 1 : -1 })
    }).then(res => res.json())
      .then(data => {
        console.log(data);
        const index = data.move.index;
        const isiBaruAI = isi.slice();
        isiBaruAI[index] = giliranAI;
        const historiBaruAI = [...histori, isiBaruAI];
        setHistori(historiBaruAI);
        setIsi(isiBaruAI);
        setMove(historiBaruAI.length - 1);
      })
  }

  function getAISRC(isi, giliranAI) {
    setTimeout(() => {
      const aiMove = findBestMove(isi.slice(), giliranAI);
      if (aiMove !== -1) {
        const isiBaruAI = isi.slice();
        isiBaruAI[aiMove] = giliranAI;
        const historiBaruAI = [...histori, isiBaruAI];
        setHistori(historiBaruAI);
        setIsi(isiBaruAI);
        setMove(historiBaruAI.length - 1);
      }
    }, 500);
  }

  useEffect(() => {
    if (giliranAI == (giliranX ? 'X' : 'O') && !cekPemenang(isi) && isi.includes(null)) {
      if (jenisAI === "Minimax") {
        getAISRC(isi, giliranAI);
      } else if (jenisAI === "AIRL") {
        getAIRL(isi, giliranAI)
      }
    }
  }, [move, isi, histori, giliranX, giliranAI]);

  const undo = () => {
    if (histori.length <= 2) return alert("belum mulai, tidak bisa undo");
    setIsi(histori[move - 2])
    setHistori(histori.slice(0, histori.length - 2))
    setMove(move - 2)
  }

  const reset = () => {
    setIsi(histori[0])
    setMove(0)
    setHistori(histori.slice(0, 1))
  }

  console.log("rendered")
  const pemenang = cekPemenang(isi);
  if (pemenang && pemenang !== 'Seri') {
    alert("Pemenang: " + pemenang);
    reset();
  } else if (pemenang === 'Seri') {
    alert("Game berakhir dengan hasil seri!");
    reset();
  }
  return (
    <>
      <div className='judul'>
        <h3>Pilih Jenis AI :</h3>
        <select name="jenisAI" defaultValue={"Minimax"} onChange={(e) => { reset(); setJenisAI(e.target.value) }}>
          <option value="Minimax">Minimax</option>
          <option value="AIRL">AIRL</option>
          <option value="Random">Tanpa AI</option>
        </select>
      </div>
      <div className='judul'>
        <h3>Pilih Giliran :</h3>
        <select name="giliran" defaultValue={"O"} onChange={(e) => { reset(); setGiliranAI(e.target.value) }}>
          <option value="O">X</option>
          <option value="X">O</option>
        </select>
      </div>
      <div className='status'>
        {"Giliran : " + (giliranX ? "X" : "O")}
        <button className="btn" onClick={undo}>Undo</button>
        <button className="btn" onClick={reset}>Reset</button>
      </div>
      <div className="App">
        {isi.map((val, i) => (
          <Square key={i} value={val} klik={() => handleClick(i)} />
        ))}
      </div>
    </>
  );
}