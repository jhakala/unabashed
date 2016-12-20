on run {input, parameters}
  set inputPath to POSIX path of input
  tell application "iTerm"
    activate
    select first window
    tell current window
      set newTab to (create tab with default profile)
      tell current session
        write text "pyroot " & quote & inputPath & quote
        write text "TBrowser() "
      end tell
    end tell
  end tell
end run
