/* MOEDA 3D REALISTA GIRANDO */
.coin-main {
    width:180px; 
    height:180px; 
    margin:40px auto; 
    position:relative; 
    transform-style:preserve-3d; 
    animation:rotate3d 3s linear infinite, float 3s ease-in-out infinite; /* 3s = mais rápida */
}
@keyframes rotate3d { 
    from {transform: rotateY(0deg) rotateX(15deg);} 
    to {transform: rotateY(360deg) rotateX(15deg);} 
}
@keyframes float { 
    0%,100%{transform:translateY(0) rotateY(0deg)} 
    50%{transform:translateY(-30px) rotateY(180deg)} 
}
.coin-face {
    position:absolute; 
    width:100%; 
    height:100%; 
    border-radius:50%; 
    background: radial-gradient(circle at 25% 25%, #fff8c0 0%, #ffd700 30%, #ffaa00 70%, #b8860b 100%); 
    border:3px solid #ffed4e; 
    box-shadow: 0 0 50px #ffd700, inset 0 0 40px rgba(255,255,255,0.5), inset 0 -15px 25px rgba(0,0,0,0.4); 
    display:flex; 
    align-items:center; 
    justify-content:center; 
    font-size:70px; 
    color:#8B6914;
    backface-visibility: hidden; /* pra não espelhar */
}
.coin-front {transform: translateZ(15px);}
.coin-back {transform: rotateY(180deg) translateZ(15px);}
.coin-rim {
    position:absolute; 
    width:100%; 
    height:100%; 
    border-radius:50%; 
    background: repeating-conic-gradient(from 0deg, #ffd700 0deg 5deg, #ffaa00 5deg 10deg); /* mais detalhes */
    transform: rotateY(90deg) translateZ(15px);
}