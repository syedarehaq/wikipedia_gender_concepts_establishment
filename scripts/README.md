### First create the chunked files from one input file
The raw input file do not have any header, Laura ssend me the files without any header everytime. I put the raw input file in the ./input/raw/ directory.
Then run the following script:
```
python3 05_01_02_create_chunks_of_concepts_from_single_file.py -C brown_phrases_oneword
```
where `brown_phrases_oneword` is an example raw input file.

### Then create chunk for each idle machine in discovery cluster
We have a default set of nodelist based on whether they are idle or not. Then based on those nodes names, we create a file that contains a list of files containging the concepts that each discovery node will search for.
```
python3 05_02_03_select_chunks_for_each_node_discovery_direct_nodename_from_nodelist.py -C brown_phrases_oneword
```