<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IGNI-15 V15.0 SUPREMA - SISTEMA TÁTICO 3D</title>
    <!-- Bibliotecas de Alto Desempenho para 3D e Fontes -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    
    <style>
        /* === CONFIGURAÇÕES DE GUERRA (CSS MILITAR 3D) === */
        :root {
            --gold: #FFD700;
            --cyber-cyan: #00ffff;
            --bg-dark: #050505;
            --panel-bg: rgba(10, 10, 10, 0.85);
            --alert-green: #00ff41;
        }

        * { box-sizing: border-box; }

        body {
            background: var(--bg-dark);
            color: #fff;
            font-family: 'Orbitron', 'Courier New', monospace;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            position: relative;
            min-height: 100vh;
        }

        /* Fundo 3D do Three.js */
        #canvas-container {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 0;
            pointer-events: none; /* Permite clicar nos botões */
            background: radial-gradient(circle at center, #111 0%, #000 100%);
        }

        /* Camada de Interface (Fica acima do 3D) */
        .ui-layer {
            position: relative;
            z-index: 10;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            padding: 30px 0 20px 0;
            border-bottom: 2px solid rgba(255, 215, 0, 0.2);
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 3.5rem;
            margin: 0;
            color: var(--gold);
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.6), 0 0 60px rgba(255, 215, 0, 0.3);
            letter-spacing: 5px;
        }

        .header .subtitle {
            color: var(--cyber-cyan);
            font-size: 0.9rem;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
            margin-top: 10px;
        }

        /* Painéis de Vidro (Glassmorphism Tático) */
        .panel {
            background: var(--panel-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 215, 0, 0.2);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 25px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.8), inset 0 0 30px rgba(255, 215, 0, 0.05);
            transition: all 0.3s ease;
        }

        .panel:hover {
            border-color: rgba(255, 215, 0, 0.5);
            box-shadow: 0 15px 35px rgba(0,0,0,0.8), 0 0 20px rgba(255, 215, 0, 0.2);
        }

        .panel h2 {
            font-size: 1.2rem;
            color: var(--cyber-cyan);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 10px;
            margin-top: 0;
            letter-spacing: 2px;
            display: flex;
            align-items: center;
        }

        /* Layout de Saldos */
        .balance-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }

        .balance-item {
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid #333;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .balance-item span { display: block; font-size: 1.5rem; color: var(--gold); margin-top: 5px; }

        /* Inputs e Botões (Alta Resolução) */
        input {
            width: 100%;
            padding: 15px;
            margin-bottom: 15px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #333;
            border-radius: 8px;
            color: #fff;
            font-family: 'Orbitron', monospace;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s;
        }
        input:focus { border-color: var(--gold); box-shadow: 0 0 15px rgba(255, 215, 0, 0.3); }

        button {
            width: 100%;
            padding: 18px;
            margin-top: 5px;
            background: linear-gradient(135deg, #B8860B 0%, var(--gold) 100%);
            border: none;
            border-radius: 8px;
            color: #000;
            font-family: 'Orbitron', monospace;
            font-weight: bold;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
        }

        /* Botões Secundários (Controle Chain) */
        .btn-cyan {
            background: transparent;
            border: 1px solid var(--cyber-cyan);
            color: var(--cyber-cyan);
            margin-bottom: 10px;
        }
        .btn-cyan:hover { background: rgba(0, 255, 255, 0.1); box-shadow: 0 0 30px rgba(0, 255, 255, 0.4); }

        /* Terminal de Logs */
        #terminal {
            background: #000;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 15px;
            height: 180px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            color: #aaa;
            margin-top: 15px;
            line-height: 1.5;
        }
        #terminal .log-info { color: #fff; }
        #terminal .log-success { color: var(--alert-green); text-shadow: 0 0 5px rgba(0, 255, 65, 0.4); }
        #terminal .log-gold { color: var(--gold); text-shadow: 0 0 5px rgba(255, 215, 0, 0.4); }
        #terminal .log-error { color: #ff3333; text-shadow: 0 0 5px rgba(255, 51, 51, 0.4); }

        /* Saída do Plano Tático */
        #plano-output {
            background: rgba(0,0,0,0.5);
            border-left: 4px solid var(--cyber-cyan);
            padding: 15px;
            margin-top: 15px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            color: #ccc;
        }
    </style>
</head>
<body>

    <!-- CONTAINER 3D -->
    <div id="canvas-container"></div>

    <!-- INTERFACE TÁTICA -->
    <div class="ui-layer">
        <div class="header">
            <h1>IGNI-15</h1>
            <div class="subtitle">PROTOCOLO SUPREMA | SISTEMA TÁTICO V15.0</div>
        </div>

        <div class="panel">
            <h2>🧠 MEMÓRIA TÁTICA</h2>
            <p style="color:#eee;">Leitura: <strong style="color:var(--gold);">{{memoria.meta_leitura}}</strong></p>
            <p style="color:#eee;">Renda: <strong style="color:var(--gold);">{{memoria.meta_renda}}</strong></p>
        </div>

        <div class="panel">
            <h2>💰 SALDOS DA REDE</h2>
            <div class="balance-grid" id="saldos-container">
                <div class="balance-item">Alice <span id="bal-alice">1000</span></div>
                <div class="balance-item">Bob <span id="bal-bob">1000</span></div>
                <div class="balance-item">Comandante <span id="bal-comandante">10000</span></div>
            </div>
        </div>

        <div class="panel">
            <h2>🚀 CRIAÇÃO DE TRANSAÇÃO</h2>
            <input type="text" id="destinatario" placeholder="Destinatário" value="Bob">
            <input type="number" id="quantidade" placeholder="Quantidade" value="50">
            <button onclick="enviarTransacao()">EXECUTAR TRANSFERÊNCIA</button>
        </div>

        <div class="panel">
            <h2>⚙️ CONTROLE DA CHAIN</h2>
            <button class="btn-cyan" onclick="minerarBloco()">MINERAR BLOCO (CONSENSO)</button>
            <button class="btn-cyan" onclick="verChain()">VER CHAIN COMPLETA</button>
            <button class="btn-cyan" onclick="verificar()">VERIFICAR VALIDADE</button>
        </div>

        <div class="panel">
            <h2>📈 PLANO TÁTICO</h2>
            <button onclick="gerarPlano()">GERAR PLANO DE GUERRA 10K</button>
            <div id="plano-output">Aguardando inicialização do protocolo...</div>
        </div>

        <div class="panel" style="border-color: #333;">
            <h2 style="color:#888;">📡 TERMINAL DE BORDA</h2>
            <div id="terminal">
                <div class="log-info">>> INICIALIZANDO SISTEMA IGNI-15...</div>
                <div class="log-info">>> CONECTADO AO MÓDULO DE GUERRA.</div>
            </div>
        </div>
    </div>

    <!-- =========== JAVASCRIPT EVOLUÍDO =========== -->
    <script>
        // --- CONFIGURAÇÃO DO MOTOR 3D (THREE.JS) ---
        function initThreeJS() {
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            container.appendChild(renderer.domElement);

            // 1. Luzes de Alto Contraste
            const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xFFD700, 1.5);
            directionalLight.position.set(5, 5, 10);
            scene.add(directionalLight);
            const backLight = new THREE.PointLight(0x00ffff, 1);
            backLight.position.set(-5, -5, -10);
            scene.add(backLight);

            // 2. Objeto Central (Bloco Dourado Giratório)
            const geometry = new THREE.IcosahedronGeometry(2, 1); // Bloco de alta tecnologia
            const material = new THREE.MeshStandardMaterial({
                color: 0xFFD700,
                wireframe: true,
                emissive: 0xFFD700,
                emissiveIntensity: 0.2,
                metalness: 0.8,
                roughness: 0.2
            });
            const icosahedron = new THREE.Mesh(geometry, material);
            scene.add(icosahedron);

            // 3. Campo de Partículas (Estrelas Douradas)
            const starsGeometry = new THREE.BufferGeometry();
            const starsCount = 1500;
            const starPositions = new Float32Array(starsCount * 3);
            for (let i = 0; i < starsCount * 3; i += 3) {
                starPositions[i] = (Math.random() - 0.5) * 100;
                starPositions[i+1] = (Math.random() - 0.5) * 100;
                starPositions[i+2] = (Math.random() - 0.5) * 100;
            }
            starsGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
            const starsMaterial = new THREE.PointsMaterial({
                color: 0xFFD700,
                size: 0.1,
                transparent: true,
                opacity: 0.8
            });
            const stars = new THREE.Points(starsGeometry, starsMaterial);
            scene.add(stars);

            camera.position.z = 7;

            // 4. Animação Tática
            function animate() {
                requestAnimationFrame(animate);
                icosahedron.rotation.x += 0.005;
                icosahedron.rotation.y += 0.01;
                stars.rotation.y -= 0.0005; // Movimento lento do fundo
                renderer.render(scene, camera);
            }
            animate();

            // Ajuste de tela
            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });
        }
        initThreeJS();


        // --- INTERAÇÃO COM O FLASK BACKEND ---

        function logTerminal(msg, type='info') {
            const terminal = document.getElementById('terminal');
            const div = document.createElement('div');
            div.className = `log-${type}`;
            const time = new Date().toLocaleTimeString();
            div.innerText = `[${time}] ${msg}`;
            terminal.appendChild(div);
            terminal.scrollTop = terminal.scrollHeight;
        }

        async function fetchAPI(url, method='GET', body=null) {
            try {
                const options = { method, headers: {} };
                if(body) { options.headers['Content-Type'] = 'application/json'; options.body = JSON.stringify(body); }
                const res = await fetch(url, options);
                return await res.text();
            } catch(e) { logTerminal("ERRO DE CONEXÃO COM O SERVIDOR", 'error'); return null; }
        }

        async function atualizarSaldos() {
            const res = await fetch('/api/saldos');
            if(res) {
                const texto = await res.text();
                // Parse do texto vindo do Python (Ex: "Alice: 1000 IGNI")
                const linhas = texto.split('<br>');
                if(linhas.length >= 3) {
                    document.getElementById('bal-alice').innerText = linhas[0].split(':')[1].replace('IGNI','').trim();
                    document.getElementById('bal-bob').innerText = linhas[1].split(':')[1].replace('IGNI','').trim();
                    document.getElementById('bal-comandante').innerText = linhas[2].split(':')[1].replace('IGNI','').trim();
                }
            }
        }

        async function enviarTransacao() {
            const de = "Comandante"; // Fixo para demonstração tática
            const para = document.getElementById('destinatario').value.trim();
            const quantidade = parseInt(document.getElementById('quantidade').value);

            if(!para || isNaN(quantidade) || quantidade <= 0) {
                logTerminal("ERRO: Parâmetros de guerra inválidos.", 'error'); return;
            }

            logTerminal(`EXECUTANDO ORDEM: ${de} -> ${para} (${quantidade} IGNI)`, 'gold');
            const res = await fetchAPI('/api/transacao', 'POST', { de, para, quantidade });
            
            if(res) {
                logTerminal(res, 'success');
                await atualizarSaldos();
            }
        }

        async function minerarBloco() {
            logTerminal("INICIANDO PROTOCOLO DE CONSENSO (MINERAÇÃO)...", 'gold');
            const res = await fetchAPI('/api/minerar', 'POST');
            if(res) {
                logTerminal(res, 'success');
                await atualizarSaldos();
            }
        }

        async function verChain() {
            logTerminal("ABRINDO VISUALIZADOR DA CHAIN...", 'info');
            window.open('/api/chain', '_blank');
        }

        async function verificar() {
            logTerminal("VERIFICANDO INTEGRIDADE DA REDE...", 'info');
            const res = await fetchAPI('/api/validar');
            if(res) logTerminal(res, 'success');
        }

        async function gerarPlano() {
            logTerminal("GERANDO PLANO ESTRATÉGICO...", 'gold');
            const res = await fetchAPI('/api/plano');
            if(res) {
                document.getElementById('plano-output').innerText = res;
                logTerminal("PLANO DE GUERRA CARREGADO COM SUCESSO.", 'success');
            }
        }

        // Inicialização
        setTimeout(() => { logTerminal("SISTEMA PRONTO PARA AÇÃO. AGUARDANDO COMANDOS.", 'success'); }, 1500);
        atualizarSaldos();

    </script>
</body>
</html> 