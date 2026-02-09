import streamlit as st
from pydub import AudioSegment
import io

st.set_page_config(page_title="Mixador de Podcast", layout="centered")

st.title("🎙️ Mixador Automático Profissional")
st.info("A voz entrará 1s após a intro e terminará 1s antes da saída, com a trilha contínua.")

# 1. Upload do Áudio do Celular
arquivo_voz = st.file_uploader("Envie seu áudio (.m4a ou .mp3)", type=["m4a", "mp3", "wav"])

if arquivo_voz:
    if st.button("Gerar Áudio Mixado"):
        with st.spinner("Processando áudio..."):
            try:
                # Carregar arquivos
                voz = AudioSegment.from_file(arquivo_voz)
                intro = AudioSegment.from_file("assets/intro.mp3")
                saida = AudioSegment.from_file("assets/saida.mp3")
                trilha = AudioSegment.from_file("assets/trilha_fundo.mp3")

                # --- LÓGICA DE MIXAGEM ---
                respiro = 1000  # 1 segundo em milissegundos
                
                # Ajustar volume da trilha
                bg = trilha - 25 
                
                # Duração: 1s + Voz + 1s
                duracao_total_meio = respiro + len(voz) + respiro
                
                # Ajustar trilha ao tamanho necessário
                bg_ajustado = (bg * (duracao_total_meio // len(bg) + 1))[:duracao_total_meio]
                
                # Mixar voz com atraso de 1s sobre a trilha
                meio_mixado = bg_ajustado.overlay(voz, position=respiro)
                
                # Unir tudo: Intro -> Bloco Mixado -> Saída
                audio_final = intro + meio_mixado + saida
                # -------------------------

                # Exportar para memória
                buffer = io.BytesIO()
                audio_final.export(buffer, format="mp3")
                
                st.success("✅ Mixagem concluída!")
                st.audio(buffer, format="audio/mp3")
                
                st.download_button(
                    label="📥 Baixar Áudio Final",
                    data=buffer.getvalue(),
                    file_name="audio_mixado_profissional.mp3",
                    mime="audio/mp3"
                )
            except Exception as e:
                st.error(f"Erro: {e}. Verifique se os arquivos na pasta assets estão corretos.")