#!/bin/bash

if [ -f Rakefile.quality ]
then
  docker run -v "$(pwd)":/usr/app -v "$(pwd)"/Rakefile.quality:/usr/quality/Rakefile apiology/quality:jumbo-latest
else
  docker run -v "$(pwd):/usr/app" apiology/quality:jumbo-latest "$@"
fi
