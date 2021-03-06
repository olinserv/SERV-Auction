SERV Auction Python Files
=========================

Instructions:
1. Generate 2 .csv files containing the live auction and silent auction items. 
2. IMPORTANT NOTE: You need specific delimiters in your csv to handle commas etc in the text. Delimiters: | as the item delimiter and % as the quote delimiter. NB: It should be possible to escape the commas such that this isn't necessary, but I (Derek) don't have time to put that into the script.
3. Column order: Name|Email Address|What are you donating?|Starting Bid|Description|Category
4. Place these .csv's into a subfolder named for the current year. The silent auction should be named FinalSilentAuction.csv and the live auction FinalLiveAuction.csv. 
5. These delimiters, filenames, subfolders, and columns can be changed in the scripts, if desired. 
6. Replace all instances of the previous year with the current year in each of the 2 Python scripts (e.g. replace "2014" with "2015").
7. Run each of the 2 scripts. Make sure that the script runs until the end (occasionally, user input will make the scripts fail and you'll have to fix whatever went wrong).
8. Compile each of the 3 resulting .tex files in your favorite LaTeX editor. Here, user input will frequently cause the LaTeX code not to compile, so you should manually fix the issue or add a new case to handle it in the code and re-run the scripts.
9. Common LaTeX problems: Special characters that need to be escaped ($&#^_ etc), non-numerical starting bids, and empty descriptions. Fix these manually in the spreadsheet or by manually post-processing the LaTeX.
10. Email redfern.derek@gmail.com with questions. I don't know the original provenance of this code but I'd be glad to help you if needed.