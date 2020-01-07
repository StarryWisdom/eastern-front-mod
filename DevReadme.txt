Philosophy
I don't know what XML parser Artemis uses, but it clearly allows some not strictly conforming XML.
It allows incorrect comments, text outside of elements, and sometimes its OK with missing element end tags.
I think its a fools errand trying to exactly match parsing of the XML out of game in game so all XML is intended to fully conforming XML.
I don't have experience in things like XSD, that would likely be a valuable tool to add, but from my limited knowledge would be insufficient to check for validity.
The zip files are built by bash scripts, this is non ideal from a platform independence stance, but it should help ensure they are built the same way each time.

Current checks
xmllint - checks that the XML is valid XML
artemis-check.py - current checks
  Errors
    hullRace ID art not increasing (this want checking to see what artemis does to see if it really should be an error, warning or nothing)
  Warnings
    Missing bases for a enemy race (makes ID 0 ships spawn as bases in siege and deep strike)
