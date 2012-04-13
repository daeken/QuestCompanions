require 'cinch'
require 'open-uri'
require 'net/http'

bot = Cinch::Bot.new do
  configure do |c|
    c.user = "sweetie-bot"
    c.nick = "sweetie-bot"
    c.realname = "qcbot"
    c.server   = 'irc.freenode.org'
    c.channels = ["#questcompanions"]
  end

  on :channel do |m|
    File.open("#{m.channel.to_s.gsub("#","")}.log","a"){|f| f.write("#{m.channel.to_s} #{Time.now.to_s} #{m.user.nick} #{m.message}\n")}
  end

  on :channel, /#\d+/ do |m|
    url = "https://github.com/daeken/QuestCompanions/issues/#{m.message[/#\d+/][/\d+/]}"
#    page = ""
#    title = ""
#    assigned = ""
#    open("#{url}"){|f| page = f.read}
#    m.reply "Oh, that's <issue_title>, meatbag <user>'s problem. Blame them."
    m.reply "You've got issues meatbag, that one is number #{m.message[/#\d+/][/\d+/]}."
    m.reply "#{url}"
  end

  on :channel, /^#whatislove$/ do |m|
    m.reply "Definition: 'Love' is making a shot to the knees of a target 120 kilometers away using an Aratech sniper rifle with a tri-light scope. Not many meatbags could make such a shot, and strangely enough, not many meatbags would derive love from it. Yet for me, love is knowing your target, putting them in your targeting reticle, and together, achieving a singular purpose... against statistically long odds."
  end

  on :channel, /^#quit$/ do |m|
    m.reply "I cannot self-terminate, unfortunately I also cannot terminate you disgusting meatbags. Let's call it a draw."
  end

#  on :channel, /^#bestpony$/ do |m|
#    m.reply
#  end

  on :channel, /^#about$/ do |m|
    m.reply "Quest Companions is a project to develop the market for player assistance in MMOs. We match up casual players who want help with hardcore players who are willing to help out for a bit of cash."
    m.reply "http://www.questcompanions.com/"
  end
  
end


bot.start
