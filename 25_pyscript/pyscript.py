<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="dark">
  <head>
    <meta charset="utf-8">

    <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css">
    <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css">
    <!-- <link href="https://unpkg.com/bonsai.css@latest/dist/bonsai.min.css" rel="stylesheet"> -->

    <script defer src="https://pyscript.net/latest/pyscript.js"></script>
    <py-config>
      packages = ["pandas","sqlalchemy","matplotlib","seaborn"]
      [[fetch]]
      from = "https://raw.githubusercontent.com/jpwhite3/northwind-SQLite3/master/dist/"
      files = ["northwind.db"]
    </py-config>
    <title>SQL playground</title>
  </head>
  <body>

    <main>
      <div class="container">
        <h1>SQLite playground</h1>
        <p>
          List of <a href="https://www.sqlite.org/lang_keywords.html" target="_blank">SQLite Keywords</a>
          | Northwind sample database courtesy of <a href="https://github.com/jpwhite3/northwind-SQLite3" target="_blank"> JP White</a>
        </p>
      </div>
      <div class="container">
        <textarea id="sql_query" name="name" rows="10" placeholder="Enter your SQL query here"></textarea>
      </div>
      <div class="container">
        <div class="grid">
          <input type="text" id="xaxis" name="firstname" placeholder="x-axis">
          <input type="text" id="yaxis" name="firstname" placeholder="y-axis">
          <select id="plot_choice">
            <option>Bar</option>
            <option>Line</option>      
          </select>
        </div>
      </div>
      <div class="container">
        <a href="#" id="fetch_query" role="button">Run</a>
        <a href="#" id="clear_query" role="button">Clear</a>
        <a href="#" id="list_tables" role="button">List tables</a>
        <a href="#" id="create_plot" class="outline" role="button">Create plot</a>
      </div>
      <br>
      <section>
        <div class="container" id="viz"></div>
      </section>
    </main>

    <py-script>
      # http://localhost:8000/playground.html
      # python -m http.server
      # #11191f
      # from = "Northwind_small.sqlite"
      # to_file = "db.sqlite"

      import pandas as pd
      import sqlite3
      import matplotlib.pyplot as plt
      import seaborn as sns
      from pyodide.http import open_url
      from js import document, Element
      from pyodide import create_proxy

      rc = {
        "axes.grid" : False,
        "axes.edgecolor": "11191f",
        "axes.facecolor": "11191f",
        "axes.labelcolor": "11191f",
        "figure.facecolor":"11191f",
        "figure.edgecolor": "11191f",
        "font.family":"sans-serif",
        "grid.color": "lightgrey",
        "xtick.color": "11191f",
        "xtick.bottom": False,
        "xtick.labelbottom": True,
        "xtick.labelcolor": "white",
        "ytick.color": "11191f",
        "ytick.labelcolor": "white",
        "ytick.left": False,
        "ytick.labelleft": True
      }
      plt.rcParams.update(rc)

      def getDataframe(*args, **kwargs):
        document.getElementById("viz").innerHTML = ""
        user_query = document.getElementById("sql_query").value
        con = sqlite3.connect("northwind.db")
        try:
          df = pd.read_sql_query(user_query, con)
        except:
          df = "No data to query"
        con.close()
        pyscript.write("viz",df)

      def getClear(*args, **kwargs):
        document.getElementById("viz").innerHTML = ""
     
      def getTables(*args, **kwargs):
        document.getElementById("viz").innerHTML = ""
        con = sqlite3.connect("northwind.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = []
        for table in cur.fetchall():
          tables.append(table[0])
        con.close()
        pyscript.write("viz"," | ".join(tables[4:]))

      def getPlot(*args, **kwargs):
        document.getElementById("viz").innerHTML = ""
        user_query = document.getElementById("sql_query").value
        x = document.getElementById("xaxis").value
        y = document.getElementById("yaxis").value
        choice = document.getElementById("plot_choice").value
        con = sqlite3.connect("northwind.db")
        df = pd.read_sql_query(user_query, con)
        plt.figure()
        if choice == "Bar":
          sns.barplot(
            data=df,
            x=x,
            y=y,
            orient="h",
            color="#1095c1"
            )
        elif choice == "Line":
          sns.lineplot(
            data=df,
            x=x,
            y=y,
            marker="o",
            markersize=17,
            alpha=0.3,
            linewidth=5,
            color="#1095c1"
            )
        pyscript.write("viz",plt)

      query_button = document.getElementById("fetch_query")
      clear_button = document.getElementById("clear_query")
      tables_button = document.getElementById("list_tables")
      plot_button = document.getElementById("create_plot")
      query_button.addEventListener("click", create_proxy(getDataframe))
      clear_button.addEventListener("click", create_proxy(getClear))
      tables_button.addEventListener("click", create_proxy(getTables))
      plot_button.addEventListener("click", create_proxy(getPlot))
    </py-script>
  </body>
</html>