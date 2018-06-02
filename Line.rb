# read command from standard input:
while cmd = STDIN.gets
  # remove whitespaces:
  cmd.chop!
  # if command is "exit", terminate:
  if cmd == "exit"
    break
  else
    # else evaluate command, send result to standard output:
    print send_msg(cmd),"\n"
    # and append [end] so that master knows it's the last line:
    print "[end]\n"
    # flush stdout to avoid buffering issues:
    STDOUT.flush
  end
end

def send_msg(msg)
  browser.send_keys :enter
  browser.send_keys msg
  browser.send_keys :enter
  return 'success'
end


$get = "init"
$count = 0
$users = Array.new
$index
loop do
    # last_msg = browser.divs(css: ".MdRGT07Cont.mdRGT07Other").last
    if browser.divs(css: ".MdRGT07Cont").last.attribute_value("data-local-id")!= $get
        if not browser.divs(css: ".mdRGT07Body .mdRGT07Ttl").last.text.include?(users)
            users.push(browser.divs(css: ".mdRGT07Body .mdRGT07Ttl").last.text)
            $index = -1
        else
            $index = users.index(browser.divs(css: ".mdRGT07Body .mdRGT07Ttl").last.text)
            
        if browser.divs(css: ".MdRGT07Cont").last.div(css:".mdRGT07Body .mdRGT07Msg.mdRGT07Image").present?
            $count += 1
            browser.buttons(id:"_chat_message_image_save").last.click
            sleep(1)
            f = Dir.entries(Dir.pwd).reject{|f|File.ftype(f)!='file'}.sort_by{|f| File.mtime(f)}.last
            File.rename(f, "#{$index}.jpg") if Time.now-File.mtime(f)<3
            $get = browser.divs(css: ".MdRGT07Cont").last.attribute_value("data-local-id")
        end
        
        if (last_text=browser.divs(css: ".MdRGT07Cont").last.div(css:".mdRGT07Body .mdRGT07Msg.mdRGT07Text")).present?
            puts last_text.span.text
            # last_text.span.text
            $get = browser.divs(css: ".MdRGT07Cont").last.attribute_value("data-local-id")
        end
    end
end