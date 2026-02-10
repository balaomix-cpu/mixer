import streamlit as st
from pydub import AudioSegment
import io
import os

# Configuração da página
st.set_page_config(page_title="Mixador Profissional", page_icon="🎙️")

st.title("🎙️ Mixador de Áudio")
st.write("A trilha de fundo tocará continuamente sob sua voz.")

# Upload do áudio enviado pelo celular
arquivo_voz = st.file_uploader("Envie seu áudio (.m4a, .mp3 ou .wav)", type=["m4a", "mp3", "wav"])

if arquivo_voz:
    st.audio(arquivo_voz, format='audio/m4a')
    
    if st.button("✨ Gerar Mixagem Final"):
        with st.spinner("Processando..."):
            try:
                # 1. Carregar a voz enviada
                voz = AudioSegment.from_file(arquivo_voz)
                
                # Caminhos dos arquivos
                path_intro = "assets/intro.mp3"
                path_saida = "assets/saida.mp3"
                path_trilha = "assets/trilha_fundo.mp3"

                # Verificar se os arquivos existem
                if not os.path.exists(path_trilha):
                    st.error(f"Arquivo {path_trilha} não encontrado na pasta assets!")
                else:
                    intro = AudioSegment.from_file(path_intro)
                    saida = AudioSegment.from_file(path_saida)
                    trilha_base = AudioSegment.from_file(path_trilha)

                    # --- CONFIGURAÇÃO DA MIXAGEM ---
                    respiro = 1000  # 1 segundo de folga nas pontas
                    
                    # Ajustar volume da trilha de fundo para -15dB (mais audível que antes)
                    bg_volume = trilha_base - 15 
                    
                    # Duração total do bloco do meio: 1s + voz + 1s
                    tempo_total_meio = respiro + len(voz) + respiro
                    
                    # Cortar a trilha_fundo.mp3 exatamente nesse tamanho total
                    # Se for curta, ela repete. Se for longa, ela corta.
                    bg_camada_fundo = (bg_volume * (tempo_total_meio // len(bg_volume) + 1))[:tempo_total_meio]
                    
                    # Aplicar fade out suave na trilha antes de acabar
                    bg_camada_fundo = bg_camada_fundo.fade_out(1000)

                    # A SOBREPOSIÇÃO (OVERLAY)
                    # Colocamos a VOZ sobre a TRILHA_FUNDO, começando após 1 segundo
                    bloco_misto = bg_camada_fundo.overlay(voz, position=respiro)
                    
                    # Montagem final em linha do tempo
                    audio_final = intro + bloco_misto + saida
                    # -------------------------------

                    # Exportar para memória
                    buffer = io.BytesIO()
                    audio_final.export(buffer, format="mp3")
                    
                    st.success("✅ Mixagem pronta!")
                    st.audio(buffer, format="audio/mp3")
                    
                    st.download_button(
                        label="📥 Baixar Áudio Final",
                        data=buffer.getvalue(),
                        file_name="mixagem_completa.mp3",
                        mime="audio/mp3"
                    )
                    
            except Exception as e:
                st.error(f"Erro técnico: {e}")

st.caption("Certifique-se de que trilha_fundo.mp3 está na pasta assets.")
