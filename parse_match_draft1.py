import subprocess
import os
'''
The .jar files were compiled using maven 3.6.3, Java 1.8.0.0_252
'''
if __name__=='__main__':

    test_file=os.path.dirname(__file__)+"/test_files/5528683650.dem"

    # parse the match .dem file into a txt files
    out_combat=os.path.dirname(__file__)+"/test_files/5528683650_combat.txt"
    out_info=os.path.dirname(__file__)+"/test_files/5528683650_info.txt"
    out_lifestate=os.path.dirname(__file__)+"/test_files/5528683650_lifestate.txt"
    out_matchend=os.path.dirname(__file__)+"/test_files/5528683650_matchend.txt"

    base='java -jar {} > {}'

    parsers=['combatlog.one-jar.jar',
             'info.one-jar.jar',
             'lifestate.one-jar.jar',
             'matchend.one-jar.jar']
    parsers=['/clarity_jars/'+parser for parser in parsers]
    outputs=[out_combat, out_info, out_lifestate, out_matchend]
    for parser,out in zip(parsers,outputs):
        #print(base.format(parser,out).split()) 
        s = subprocess.call("java -jar "+os.path.dirname(__file__)+\
            parser + " "+test_file\
            + ">" +out,
            shell = True) 
        print(", return code", s)     


