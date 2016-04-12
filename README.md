<h1> O.G.B.Automation_Tool </h1>
<p>A automation tool for opengamebenchmarks.org</p>

<h2>Objective</h2>
This tool was created to with the goal of automate the upload of benchmarks to Open_Game_Benchmarks, for it need to get general system information that is especified in the site of OGB and the amount of RAM and VRAM in the system. Also launch the game+benchmark tool, the aplications are terminated after the conclusion of the benchmark in Linux, using it in Windows the applications remain open after the end of benchmark. Informations about what is needed to implement in the tool are in <a href="https://github.com/Edmene/O.G.B.Automation_Tool/issues" target="new">issues</a>. Please visit <a href="https://github.com/wbasile/Open-Game-Benchmarks" target="new">Open_Game_Benchmark</a> to know more about the project.


<h2>What is need to make the tool work</h2>
<h3>The following python packages are needed for the tool to work:</h3>
<ul>
 <li>urllib</li>
 <li>bs4</li>
 <li>subprocess</li>
 <li>re</li>
 <li>django</li>
 <li>os</li>
 <li>time</li>
 <li>threading</li>
 <li>sqlite3</li>
 <h4>Linux specific:</h4>
 <li>lxml</li>
 <h4>Windows specific:</h4>
 <li>html.parser</li>
 <li>pywin32, is also possible to install it by installing pywinauto</li>
</ul>
<h4>Other needed software:</h4>
<ul>
 <li>Voglperf</li>
 <li>Glxosd</li>
 <li>Xautomation(xte)</li>
 <li>SQLite</li>
 <h4>Windows specific:</h4>
 <li>Fraps</li>
</ul>
