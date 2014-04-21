# Text Based Potentials from flickr image descriptions of PASCAL visual object classes

### Background

[This](http://tamaraberg.com/papers/generation_cvpr11.pdf) 
paper presents a system to automatically generate natural language description from images that explots both statistics gleaned from parsing large quantities of text data and recognition algorithms from computer vision. 

### Contribution
The file flickr.py is an implementation of the section 5.2 from the above paper. 

- Around 5000 flickr image descriptions were collected based on each of the PASCAL 2010 object categories.
- Each sentence from this description set is parsed by Stanford dependency parser to generate the parse tree and dependency list for the sentense.
- Collected statistics about the occurance of each attribute and object pair using the adjectival modifier dependency `amod(attribute,object)` 
- Counts for synonyms of object and attribute terms are merged together.
