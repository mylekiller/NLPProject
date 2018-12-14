Theres a lot to run to get to the final output.

Right now if the data is added to the repository the translate.py can be run directly.

What we did to get the data is first run generatedatapairs.py on train.csv and translatedenglish.txt

Then, run align.py on pairs.out 

Then, run createSCFG.py on pairs.out align.out

Then, run cleanSCFG on that output.

Finally you are ready to use that cleanSCFG file to do translations.

align is based on hw5 everything else is based on the lecture 15 notes

Many sentences will stall if a translation is attempted especially if they are too long or have too many very common words. 
