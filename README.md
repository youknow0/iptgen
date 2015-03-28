iptgen
=====

iptgen is a flexible and lightweight iptables/ip6tables rule generator.

**iptgen is not ready-to-go software.** It is more like a framework you 
have to extend to fit your needs. It is not the right tool if you
are just getting started with iptables. It is targeted at experienced
iptables users who want to generate very complex rule sets out of a
rather simple configuration file.

Features
----

* Very flexible. You want physdev matches in all your rules? No
  problem, just write a hook does that (see config.py)!

* Your IPv6 rules are mostly the same as your IPv4 rules? No need to
  write the same rules twice. iptgen can generate iptables and 
  ip6tables rules from the same rules file.

* You do not need iptgen on the system you want to use the rules on.
  It will generate a file that iptables-restore can understand. Thus,
  you get all the advantages: save apply using iptables-apply and a
  text file, that can be edited manually (or by script) after it has 
  been generated.

The framework
----

**Parsers** are Python classes that are used to parse a rule file. The 
parsers are then used by their respective **generator**, which will
then produce the iptables rules. You will write a new **parser** and
**generator** if you wanted to introduce a new kind of rule, for 
example a deny rule, which iptgen doesn’t provide by default.

iptgen comes with a few parsers and generators. It is very likely that
these fit your needs, but it is just as likely that you won’t like 
them. This is not a problem, because you can just comment out the 
respective import statement in the config file and write your own
generator or parser.

On the other hand, there are **hooks**. Hooks extend existing 
generators. This is useful if there is already a generator that mostly
does what you want. For example, a hook could add physdev matches your
rules. You can find examples in the config file.

The general idea is that you keep your customizations in new files and
you don’t have to edit any of the files iptgen comes with. That way
you can always do git pull to get the newest version without having to
merge your local changes with mine.
