Horton Slab Write-up Thingy
===========================

Introduction
------------

Don't expect this to *be* anything... it's just a bunch of relatively-disconnected words about what was going through my head at various times during the project, and how I fixed it, which I'm writing at the request of the professor. More or less...

Glyph shape
-----------

Each glyph is a Python class which, when instantiated, knows the properties of the glyph (weight, cap-height, slant, etc.). Using this information, it constructs the geometry of the glyph, which is made by combining two different primitives: *line* and *circle*. Both of these primitives can also be clipped by arbitrary polygons (this is how the C is constructed, for example: by taking a circle and clipping out a triangular wedge from it).

Geometry manipulation (basic boolean stuff; almost always either union, intersection, or difference) is done with the Shapely library, because I really didn't want to do that myself, as it's not very interesting.

Each glyph has a function which calculates its width relative to one em, information which is used heavily during the drawing phase.

The glyph shape function can be either very complicated (like, say, 2) or very simple, like that of the lowercase l:

    mainLine = Line(self.p(0.5, 1.0), self.p(0.5, 0.0),
                    self.weight(), serif=5)
    return [mainLine]

That's a very simple one. 2, in comparison, is about 50 lines long...

The line constructor that you see above takes three required arguments: the location of both endpoints, and the weight of the line to be drawn. The optional *serif* argument adds serifs, which we'll talk about later.

The 'p' function (I needed a really short name because I call it hundreds of times and wanted it to be neat - think of it as 'position') that I call there takes a percentage position (0.0 to 1.0) in x and y (measured from the bottom left, like things *should* be done) and turns it into coordinates in the glyph's coordinate space. p also takes another argument which determines whether it should consider the top of the glyph to be at the cap-height or the x-height.

Many of the glyphs have small adjustments that are made to the shape of the glyph as the weight changes, in order to correct for unpleasant effects.

So, the l above makes a line from the top, halfway across the glyph, to the bottom, halfway across the glyph, at the full weight of the glyph, with the 5th serif type, which will be described below.

You can look at the rest of the glyph functions on GitHub:

Capitals: http://github.com/hortont424/phiface/blob/master/phiface/capitals.py
Lowercase: http://github.com/hortont424/phiface/blob/master/phiface/lowercase.py
Numerals: http://github.com/hortont424/phiface/blob/master/phiface/numerals.py
Punc.: http://github.com/hortont424/phiface/blob/master/phiface/punctuation.py

Strange or Missing Glyphs
-------------------------

I added center-dot (for multiplication) and interrobang (at the request of my roommates) to the normal set of glyphs.

My 0 is too wide, but I couldn't bring myself to make it an oval (or, more likely, similar to the shape of the 6 or 9).

My angle-brackets are huge. HUGE! Maybe I'll fix them someday.

I'm missing curly braces, because they'd be really annoying to draw. Much worse than 2, which was enough of a pain that I don't want to endure it again.

Serifs
------

Serifs are actually added by the line drawing logic - each character doesn't really need to know how to draw a serif, it just needs to know what kind of serif it wants, and asks politely for that. There are 6 kinds of serifs a glyph can ask for on one of its lines:

    0 - No serifs
    1 - A vertical half serif on one end of the line. (E)
    2 - A vertical half serif on both ends of the line. (T)
    3 - A full serif on one end of the line. (A)
    4 - A full serif on both ends of the line. (H)
    5 - A full serif on one end of the line, a half serif on the other. (l)
    6 - A half serif on one end of the line. (j)

The fact that glyphs don't know about serifs is neat, because it means we can turn *off* the serifs very easily, by just asking Line not to draw any! That's how we get the sans-serif variant, which isn't on the poster, but that's ok...

Properties
----------

PHI = 1.618... (golden ratio)

Fixed glyph properties are as follows:

    1 em = capHeight / PHI
    xHeight = capHeight / PHI

The defaults for variable glyph properties are as follows:

    weight = 3 (this is a unitless measure, where ultralight = 0.5 and heavy = 7)
    slanted = False (not really italic, it's more *slanted* than anything)
    outlined = False (this was more for testing, but turned it into outlines)
    color = Black (obvious)
    serifed = True (whether or not Line should draw serifs for this glyph)
    autoKern = True (you'll see, in a bit)

Italic
------

The italic variant isn't nearly as neat as all the rest, it's just made quite literally by shearing the character with Cairo while it's being drawn. Not interesting, not particularly awesome, but it worked out OK. There's a pretty good chance it will break the consistency of inter-word spacing, but I'm not totally sure how to fix that (without doing the shearing beforehand, with Shapely... or manually).

Weights
-------

Technically, you can generate glyphs of whatever weight you want, because it's all procedurally generated. However, I blessed a few weights so that I didn't have to look at/tweak more than a few weights:

Ultralight = 0.5
Light = 2.0
Regular = 3.0
Bold = 5.0
Heavy = 7.0

Kerning
-------

Kerning was a stickling point for the first few days. At that point, I was just throwing glyphs down and advancing the x position by the reported width of the glyph. We all know why this doesn't work, though, with the AV pair being the classic example.

So, instead, I wrote an optical autokerner in a few lines of Python. It works by placing the two glyphs on a plane and shifting them back and forth until it finds the boundary where they're *just* touching, then adds the correct amount of kerning. There's a kerning table which gives adjustments relative to this value, but it only has a handful of entries (one case which was particularly problematic was +=, where the bar of the plus slid directly into the middle slot of the equal-sign, kerning them *way* too tightly). It could probably do with a few entries, but after all this, I didn't have a lot of time to work on the kerning table, and I didn't really think it looked *terrible* - at least not enough to worry about.

There's another issue with the optical autokerning: punctuation. Tiny little dots don't autokern well at all; also, quotes don't ever collide with lowercase letters, so that breaks things too... So I added a per-glyph override which instead kerns based on the bounding box of the glyph extended to basically-infinity in the vertical direction. This mostly fixes the problems with punctuation.

The autokerner is really quite slow (as you might expect), especially for large blocks of text, so there's a disk-based cache that stores the kerning values between runs. You have to delete it if you change the glyph shape, or your kerning will be horribly wrong. Also, the cache is per-capHeight-per-weight (as kerning values change slightly), so if you change the capHeight or weight, get ready to *wait* again...

Layout
------

The space character is also a glyph - it's a square block which is special-cased to not be drawn at all in the drawing logic. This fixed a lot of trouble I was having when advancing words in the "stupid" way (just adding some amount of x-advance each time you see a space character), where the space between the words ended up varying significantly, which was really tripping up reading.

My line-breaking algorithm is horribly primitive: it just draws words at a time; when it gets to each word, it checks to see if it's past the edge of the layout box. If it is, it moves down by the leading and moves back to the left side of the box. This is a problem mostly because it means the last word on a line could be (and usually *is*) extending beyond the right side of the layout box. Also, it creates really crappy right rag unless you pay a lot of attention, because it's really not aware of the idea of rag.

If I had a ton more time, I'd implement Knuth's famous line-breaking algorithm (the one TeX uses), which is pretty much ideal, but since I don't have that kind of time, I decided against writing a poor knockoff. I've heard it's not actually *that* complicated, but... relative terms...

Input Format
------------

The main program takes an XML file with a very simple format. For example, you can see the one that makes the description of the various weights that's on the poster here: http://github.com/hortont424/phiface/blob/master/faces.xml

There are only a few tags defined:

u, l, r, b, h = Weight (ultralight, light, regular, bold, heavy)
i = Slanted/Italic
br = Newline
textbox (attributes x, y, size, width, height) = A reflowing text container
leading, tracking, size (attribute px) = Obvious text properties
color (attributes r, g, b, a) = Obvious color properties
sans, serif = Turn on/off serifs

More Stuff
----------

If you have any questions, feel free to email me.

The code is all open-source, under the relatively permissive 2-clause BSD license, which basically just says you can do what you want with it as long as you keep my copyright header around... (the terms are in LICENSE in the source directory, but they're exactly the same as all of the gazillions of other BSD projects out there).