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

  const handleClick = (i) => {
    if (isi[i] || cekPemenang(isi)) return;
    const isiBaru = isi.slice();
    isiBaru[i] = giliranX ? "X" : "O";
    const historiBaru = [...histori, isiBaru];
    setHistori(historiBaru);
    setIsi(isiBaru);
    setMove(historiBaru.length - 1);
  };

  useEffect(() => {
    if (giliranAI == (giliranX ? 'X' : 'O') && !cekPemenang(isi) && isi.includes(null)) {
      setTimeout(() => {
        const aiMove = findBestMove(isi.slice(), giliranAI); // Buat salinan papan untuk AI
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
  }, [move, isi, histori, giliranX, giliranAI]); // Tambahkan dependensi yang relevan

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

  useEffect(() => {
    console.log(histori)
    console.log(isi)
    console.log('move ' + move)
  })
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
      <h3>
        Pilih Giliran :
        <select name="giliran" defaultValue={"O"} onChange={(e) => { reset(); setGiliranAI(e.target.value) }}>
          <option value="O">X</option>
          <option value="X">O</option>
        </select>
      </h3>
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