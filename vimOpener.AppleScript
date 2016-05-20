on run {input, parameters}
  set inputPath to POSIX path of input
  tell application "iTerm"
    activate
    select first window
    tell current window
      set newTab to (create tab with default profile)
      tell current session
        write text "vim " & quote & inputPath & quote
      end tell
    end tell
  end tell
end run
