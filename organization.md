To avoid clutter, I suggest to distinguish clearly between production and experimental code (inspired by what fj did last few years).

 * Experimental code is allowed to be shitty. While writing it you should realize that it won't go into final submission, and it's quite unlikely that anybody else will use it at all. 
 * Working on production code implies responsibility for making it clean and usable by others (introducing small usage example in main, perhaps few tests even, etc.) Chances are that production code will contribute to the final submission (although it's not necessarily).
 
Production code is not allowed to depend on experimental code.
 
When introducing changes to production code, make sure that no production code is broken.
 
Also, fj suggests to restrict shell scripts and command line interface to the very entry point of the final submission. Everything else is written as python scripts and is supposed to be executed from eclipse.


Production code goes to eclipse project 'production'. 
Experimental code can be put in any other project. Typically, but not necessarily, it's '<username>_scratch'. 

When creating new _scratch project, pick 'add project directory to PYTHONPATH'. In project properties -> references, refer it to 'production' project (but not the other way around). This way you can import modules from production, but you won't pollute module name space with your stuff. So, we have star-like dependency structure, with every _scratch project depending on production (and in few rare cases _scratch project depending on another _scratch).


Same thing for data. If piece of datum is canonical or otherwise important to everybody, it goes to a designated folder ('data', i guess), and can be accessed from any project through path '../data/whatever'. Temporary or dirty data files go inside your _scratch projects (if you decide to put them under version control at all).

Commits affecting production code can be observed by 'gitk production'.


---

Yeah, as for coding conventions, rely on PEP 8.