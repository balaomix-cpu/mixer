import streamlit as st
from pydub import AudioSegment
import io
import os

# Configuração da página
st.set_page_config(page_title="Mixador Profissional v2", page_icon="🎙️")

st.title("🎙️ Mixador de Áudio Pro")
st.write("Mixagem com transições suaves e ganho de voz.")

# Upload do áudio enviado pelo celular
arquivo_voz = st.file_uploader("Envie seu áudio (.m4a, .mp3 ou .wav)", type=["m4a", "mp3", "wav"])

if arquivo_voz:
    st.audio(arquivo_voz, format='audio/m4a')
    
    if st.button("✨ Gerar Mixagem com Transições"):
        with st.spinner("Processando mixagem e ganho de áudio..."):
            try:
                # 1. Carregar a voz e aumentar o volume em 20% (+5 decibéis)
                voz = AudioSegment.from_file(arquivo_voz)
                voz = voz + 5  # Aumenta o volume da gravação
                
                # Caminhos dos ativos
                path_intro = "assets/intro.mp3"
                path_saida = "assets/saida.mp3"
                path_trilha = "assets/trilha_fundo.mp3"

                if not os.path.exists(path_trilha):
                    st.error("Arquivo de trilha não encontrado!")
                else:
                    intro = AudioSegment.from_file(path_intro)
                    saida = AudioSegment.from_file(path_saida)
                    trilha_base = AudioSegment.from_file(path_trilha)

                    # --- CONFIGURAÇÃO DA MIXAGEM ---
                    # Tempo de sobreposição para o crossfade (1000ms = 1 segundo)
                    fade_time = 1000 
                    
                    # Volume da trilha de fundo (mantido conforme seu feedback)
                    bg_volume = trilha_base - 15 
                    
                    # Duração da trilha: Voz + os tempos de fade
                    duracao_total_bg = len(voz) + (fade_time * 2)
                    
                    # Preparar camada de fundo (loop/corte)
                    bg_camada = (bg_volume * (duracao_total_bg // len(bg_volume) + 1))[:duracao_total_bg]
                    
                    # Aplicar fade in e fade out na trilha de fundo para suavizar a entrada/saída
                    bg_camada = bg_camada.fade_in(fade_time).fade_out(fade_time)

                    # Sobrepor a voz no meio da trilha
                    # A voz entra exatamente após o tempo de fade inicial
                    bloco_misto = bg_camada.overlay(voz, position=fade_time)
                    
                    # --- MONTAGEM COM CROSSFADE ---
                    # Usamos append com crossfade para fundir a Vinheta com a Trilha/Voz
                    # Isso elimina o "espaço" e faz um som entrar enquanto o outro sai
                    passo1 = intro.append(bloco_misto, crossfade=fade_time)
                    audio_final = passo1.append(saida, crossfade=fade_time)
                    # -------------------------------

                    # Exportar
                    buffer = io.BytesIO()
                    audio_final.export(buffer, format="mp3")
                    
                    st.success("✅ Mixagem profissional concluída!")
                    st.audio(buffer, format="audio/mp3")
                    
                    st.download_button(
                        label="📥 Baixar Áudio Editado",
                        data=buffer.getvalue(),
                        file_name="podcast_mixado_suave.mp3",
                        mime="audio/mp3"
                    )
                    
            except Exception as e:
                st.error(f"Erro: {e}")

st.caption("Volume da voz aumentado e transições suavizadas.")
