require 'cinch'
require 'json'
require 'open-uri'
require 'openssl'
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

bot = Cinch::Bot.new do
  configure do |c|
    c.user = "sweetie-bot"
    c.nick = "sweetie-bot"
    c.realname = "qcbot"
    c.server   = 'irc.freenode.org'
    c.channels = ["#questcompanions"]
  end

  on :channel, /#\d+/ do |m|
    m.message.scan(/#(\d+)/) do |(id)|
      url = "https://github.com/daeken/QuestCompanions/issues/#{id}"
      apiurl = "https://api.github.com/repos/daeken/QuestCompanions/issues/#{id}?access_token=cc7e48f94f3d30d806b5a572049937d3c51cabf2"
      open(apiurl) do |f|
        json = JSON.parse f.read
        title = json['title']
        if json['assignee'] != nil
          owner = " (#{json['assignee']['login']})"
        else
          owner = ''
        end
        m.reply "##{id} #{title}#{owner}: #{url}"
      end
    end
  end

  on :channel, /^#whatislove$/ do |m|
    m.reply "Definition: 'Love' is making a shot to the knees of a target 120 kilometers away using an Aratech sniper rifle with a tri-light scope. Not many meatbags could make such a shot, and strangely enough, not many meatbags would derive love from it. Yet for me, love is knowing your target, putting them in your targeting reticle, and together, achieving a singular purpose... against statistically long odds."
  end

  on :channel, /^#quit$/ do |m|
    m.reply "I cannot self-terminate, unfortunately I also cannot terminate you disgusting meatbags. Let's call it a draw."
  end

  on :channel, /^#about$/ do |m|
    m.reply "Quest Companions is a project to develop the market for player assistance in MMOs. We match up casual players who want help with hardcore players who are willing to help out for a bit of cash."
    m.reply "http://www.questcompanions.com/"
  end
  
end


bot.start
