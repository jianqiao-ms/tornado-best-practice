# tornado-best-practice
Best pratice using Python framework 'TORNADO', including logging configuration, command line arguments parsing and so on.

# What did I do

## Abandon tornado.options

As official description of tornado.options.OptionParser.parse_config_file, the method is **not safe**.

> The config file contains Python code that will be executed (so
it is **not safe** to use untrusted config files). Anything in
the global namespace that matches a defined option will be
used to set that option's value.

And OptionParser dose not support options group, which is not awesome at all.

So, I make new class or method to realize configurations of tornado.

##### Code details

TODO