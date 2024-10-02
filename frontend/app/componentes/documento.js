'use client'
import { useState } from "react";
import ModalDocumento from "./modalDocumento";

export default function Documento({ dados }) {
    const [modalAberta, setModalAberta] = useState(false);

    function exibirDocumento() {
        setModalAberta(true);
    };
    function fecharModal() {
        setModalAberta(false);
    };

    return (
        <div>
            <p>Título: {dados.file_name}</p>
            <p>ID: {dados.id}</p>
            <button onClick={exibirDocumento}>Ver conteúdo</button>
            {modalAberta ? (
                <ModalDocumento dados={dados} fecharModal={fecharModal}/>
            ):''}
        </div>
    );
}