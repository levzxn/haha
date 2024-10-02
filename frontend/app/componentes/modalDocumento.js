const { useState, useEffect } = require("react");

export default function ModalDocumento({ dados, fecharModal }) {
    const [iframeSrc, setIframeSrc] = useState('');

    useEffect(() => {
        async function getConteudo() {
            try {
                const conteudoConexao = await fetch(`http://localhost:8000/docs/file/${dados.id}`);
                const conteudoJson = await conteudoConexao.json();
                const conteudoDecodificado = atob(conteudoJson.content);
                
                const byteNumbers = new Uint8Array(conteudoDecodificado.length);
                for (let i = 0; i < conteudoDecodificado.length; i++) {
                    byteNumbers[i] = conteudoDecodificado.charCodeAt(i);
                }
                console.log(byteNumbers)
                const blob = new Blob([byteNumbers], { type: 'application/pdf' });
                const url = URL.createObjectURL(blob);

                setIframeSrc(url);
            } catch (error) {
                console.error("Erro ao buscar ou decodificar o conteúdo:", error);
            }
        }
        getConteudo();
    }, [dados.id]);

    return (
        <div className="fixed">
            <div>
                <h2>{dados.file_name}</h2>
                {iframeSrc && <iframe src={iframeSrc} width="100%" height="500px" title={dados.file_name}></iframe>}
                <button onClick={fecharModal}>Fechar</button>
            </div>
        </div>
    );
}
