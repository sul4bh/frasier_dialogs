"""
Resposibility:
* Extract data of interest
"""

import re


def get_director_and_writers(text):
    writers = ""
    director = ""
    scanning_writer = False
    for line in text.split("\n"):
        writer_line = re.match(".*Written by (.*)", line)
        director_line = re.match(".*Directed by (.*)", line)
        if writer_line:
            scanning_writer = True
            writers += writer_line.group(1).strip()
        elif director_line:
            scanning_writer = False
            director = director_line.group(1).strip()
        elif scanning_writer:
            writers += line.strip()

    writers = writers.replace(" & ", ",")
    return writers, director


def get_cast_dialog(transcript):
    cast_dialog_array = []
    collection_array = []
    for line in transcript.split("\n"):
        cast_dialog_line = re.match("^\s*(?P<cast>[a-zA-z]+): (?P<dialog>.*)", line)
        only_dialog_line = re.match("^\s+(?P<dialog>.*)", line)

        if cast_dialog_line:
            # skip when ':' appears outside of a dialog
            # "out of her bag:" @ http://www.kacl780.net/frasier/transcripts/season_1/episode_1/the_good_son.html
            if len(cast_dialog_line.group('cast').strip().split(' ')) > 1:
                continue
            if collection_array:
                cast_dialog_array.append({
                    "cast": collection_array[0],
                    "dialog": " ".join(collection_array[1:])
                })

            cast = cast_dialog_line.group('cast').strip()
            dialog = cast_dialog_line.group('dialog').strip()
            if cast and dialog:
                collection_array = [
                    cast,
                    dialog
                ]
        elif only_dialog_line and collection_array:
            collection_array.append(only_dialog_line.group('dialog').strip())

    cast_dialog_array.append({
        "cast": collection_array[0],
        "dialog": " ".join(collection_array[1:])
    })

    return cast_dialog_array


if __name__ == "__main__":
    test_data = [
"""
Martin: This is stupid.
Frasier: It is not.
 Martin: Look, nothing's going to happen between them anyway.
Frasier: What if it does?  He's my brother and he loves his wife!  
         Now, now, I know, I know their marriage is not exactly 
         everyone's cup of tea.  But on some twisted, bizarre level 
         it seems to work for them.  If Niles ever did anything to 
         hurt to his marriage, he's the one who'd suffer.  He's my 
         brother and I won't let him suffer!
 Martin: Hey, slow down!  You're going to miss the turn onto 
         Roosevelt. 
Frasier: Dad, I let you come along strictly on the agreement that you
         would not give directions.
 Martin: I'm not giving directions, I'm just telling you which way's
         faster.
Frasier: Roosevelt'll add ten minutes.
 Martin: In sunshine.  In rain it's faster!
Frasier: Oh what, spatial relationships change when it rains?!
 Martin: No, you've just got better traction on Roosevelt.  Of course, 
         you wouldn't have to worry about that if you'd gotten all-
         weather tires like I told you to, but no, you had to have 
         the fancy German thing...

Martin and Frasier carry on arguing.

CUT TO:

Scene Six - Maris's Mansion.
Lighning strikes, and things are heating up.  Daphne is sitting on 
the couch, staring at the fire.  Niles brings in some firewood.

  Niles: We'd better make this last, this is all that's left of the 
         wood. [Daphne begins to cry.] Oh no, don't worry, if 
         this runs out there's an antique sideboard in the drawing 
         room that I think is reproduction. [she looks at him] Oh. 
         It's Eric, isn't it?
"""
,
"""
    PREVIOUSLY

Julia confronting Roz in her booth.

  Julia: Are you trying to save Frasier from me, or are you trying to
         save him for yourself?
    Roz: Are you out of you out of your mind?
  Julia: Are you in love with him?

CUT TO:

Roz confronting Frasier at his apartment.

    Roz: It's her or me!  Tell me now, or I swear to God, I will walk 
         out of here and I will not come back!

Roz settling into her office at KPXY.

Wiswell: There's no chance you'll change your mind again, is there?
    Roz: No.  KACL is ancient history.

FADE TO:
"""]
    for dialog in test_data:
        print(get_cast_dialog(dialog))
