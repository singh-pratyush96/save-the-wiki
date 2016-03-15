# save-the-wiki
A command line tool that save Wikipedia article with images as HTML.

### Sample Run  

`Enter search parameter : Call of Duty`

##### Output :
```
Fetching search results
[0]: Call of Duty
[1]: Call of Duty 4: Modern Warfare
[2]: Call of Duty 2
[3]: Call of Duty: Zombies
[4]: Treyarch
[5]: Call of Duty: World at War
[6]: Call of Duty: Black Ops
[7]: Call of Duty: Modern Warfare 2
[8]: Call of Duty: Black Ops – Zombies
[9]: Call of Duty: Ghosts
Enter choice : 0 1 3 6
```

##### Result :
Saved Wikipedia pages of `Call of Duty`, `Call of Duty 4: Modern Warfare`, `Call of Duty: Zombies` and `Call of Duty: Black Ops`.

## Options

* `-q` or `--quiet`  
  *   Quiet mode, no prompts
  *   Default `not set`
* `-n` or `--number-search`  
  *   Number of search items to display
  *   Default `10`
* `-r` or `--regex`  
  *   Regex based search (Not available yet)
  *   Default `not set`
* `-s` or `--search-parameter`
  *   Search Querry
* `-p` or `--page-name`
  *   Page name as on Wikipedia
