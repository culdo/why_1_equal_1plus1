#!/usr/bin/ruby
require 'watir'
tstart = Time.now
download_bool = true
def send_msg(browser, msg)
    browser.send_keys :enter
    browser.send_keys msg
    browser.send_keys :enter
    return 'success'
end

prefs = {
  download: {
    prompt_for_download: false,
    default_directory: '/home/wuorsut/nptu/nptu_hackthon/face_recognition'
  }
}

browser = Watir::Browser.new :chrome, options: {prefs: prefs,options: {args: ["--load-extension=./2.1.4_0/"]}}
browser.goto "chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc/index.html"

browser.text_field(id: "line_login_email").click
browser.send_keys "george0228489372@yahoo.com.tw", :tab, "wuorsut", :enter

sleep(1) until browser.h1(class: 'mdRGT04Ttl').present?

$get = "init"
$user = "init"
last_chat = browser.divs(css: ".MdRGT07Cont").last


until last_chat.span.present? && last_chat.span.text == "over" do
    last_chat=browser.divs(css: ".MdRGT07Cont").last
    if last_chat.attribute_value("data-local-id")!= $get
        if (last_image=last_chat.div(css:".mdRGT07Body .mdRGT07Msg.mdRGT07Image")).present?
            if last_chat.div(css: ".mdRGT07Ttl").present?
                $user = last_chat.div(css: ".mdRGT07Ttl").text
            else
                $user = '我'
            end
            browser.buttons(id:"_chat_message_image_save").last.click
            sleep(1)
            f = Dir.entries(Dir.pwd).reject{|f|File.ftype(f)!='file'}.sort_by{|f| File.mtime(f)}.last
            File.rename(f, "#{$user}.jpg") if Time.now-File.mtime(f)<3
            $get = last_chat.attribute_value("data-local-id")

        end
    end
end

if cmd = STDIN.gets
    # remove whitespaces:
    cmd.chop!
    # if command is "exit", terminate:
    # if cmd == "exit"
    #     break
    # else
    # else evaluate command, send result to standard output:
    print send_msg(browser, cmd),"\n"
    # and append [end] so that master knows it's the last line:
    print "[end]\n"
    # flush stdout to avoid buffering issues:
    STDOUT.flush
    # end
end

loop do
  tnow = Time.now
  if tnow - tstart > 100
    download_bool = true
    tstart = Time.now
# read command from standard input:
  if download_bool = true
      last_chat=browser.divs(css: ".MdRGT07Cont").last
      if last_chat.attribute_value("data-local-id")!= $get
          if (last_image=last_chat.div(css:".mdRGT07Body .mdRGT07Msg.mdRGT07Image")).present?
              if last_chat.div(css: ".mdRGT07Ttl").present?
                  $user = last_chat.div(css: ".mdRGT07Ttl").text
              else
                  $user = '我'
              end
              browser.buttons(id:"_chat_message_image_save").last.click
              sleep(1)
              f = Dir.entries(Dir.pwd).reject{|f|File.ftype(f)!='file'}.sort_by{|f| File.mtime(f)}.last
              File.rename(f, "#{$user}.jpg") if Time.now-File.mtime(f)<3
              $get = last_chat.attribute_value("data-local-id")

          end
      end
      download_bool = false
    end
    if cmd = STDIN.gets
        # remove whitespaces:
        cmd.chop!
        # if command is "exit", terminate:
        if cmd == "exit"
            break
        else
        # else evaluate command, send result to standard output:
        print send_msg(browser, cmd),"\n"
        # and append [end] so that master knows it's the last line:
        print "[end]\n"
        # flush stdout to avoid buffering issues:
        STDOUT.flush
        end
    end
end
