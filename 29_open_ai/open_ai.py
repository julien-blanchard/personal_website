# **********************************************************************

from pytube import YouTube

def getVideo(video):
    yt = YouTube(video)
    streams = yt.streams.filter(
        only_audio=True,
        abr="128kbps"
        )
    try:
        streams.first().download()
    except Exception as e:
        print(e)

getVideo("https://www.youtube.com/watch?v=Djcy40bTgP4")

# **********************************************************************

pip install -U openai-whisper

# **********************************************************************

import whisper
from pprint import pprint

def getAudioToText(video):
    model = whisper.load_model("base")
    result = model.transcribe(video)
    return result

text = getAudioToText("Learning New Programming Languages  Brian Kernighan and Lex Fridman.mp4")
pprint(text)

# **********************************************************************

def getText(data):
    tokens = data.split(" ")
    x = 0
    while x <= len(tokens):
        print(" ".join(tokens[x:x+10]))
        x += 10

getText(text["text"])

# **********************************************************************

import plotly.express as px
import statistics as stats

def getSpeechPlot(audio):
    x = [a["start"] for a in audio["segments"]]
    y = [a["no_speech_prob"] for a in audio["segments"]]
    m = stats.median(y)
    s = stats.stdev(y)
    med = [m for _ in range(0,len(y))]
    up_stdev = [(m+s) for _ in range(0,len(y))]
    low_stdev = [(m-s) for _ in range(0,len(y))]
    
    fig = px.line(
        x=x,
        y=y,
        line_shape="spline",
        color_discrete_sequence=["#ffafcc"]
        )
    for line in [med,up_stdev,low_stdev]:
        fig.add_scatter(
            x=x,
            y=line,
            mode="lines",
            opacity=1,
                    line=dict(
                color="#bde0fe",
                width=3,
                dash="dash"
                )
            )
    fig.update_layout(
        title="No speech probability",
        xaxis_title="Timestamp",
        yaxis_title="Probability",
        bargap=0.01,
        showlegend=False,
        #template="seaborn",
        plot_bgcolor="#264653",
        paper_bgcolor="#264653",
        width=900,
        height=450,
        font=dict(
            family="Arial",
            size=18,
            color="white"
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=0.1,
        gridcolor="#9a8c98"
        )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=0.1,
        gridcolor="#9a8c98"
        )
    fig["data"][0]["line"]["width"]=8
    fig.show()

getSpeechPlot(text)