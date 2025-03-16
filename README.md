# booth25
booth game

# git commands 
After you've edited files, check to see what files you changed
```
git status
```

If you want to add your files to the repository 
```
git add .               // adds all of your changes
git add [filename]      // adds a specific file
```

Now that you've added your files 
```
git commit -m "your commit message"
```

Now to push your changes to the repository
```
git push
```

## branching 
To create a branch 
```
git checkout -b [your-name/branch-name]
```

To push your first commit 
```
git push -u origin [your-name/branch-name]
```
every time you push after you only need to do `git push`
