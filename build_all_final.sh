#!/bin/bash

for filename in part/*.wik
  do
  	echo !!! processing $filename ...
    pandoc $filename -f mediawiki -t latex --standalone -o ${filename%.*}.tex
    echo ... converted $filename to TeX.
  done
  
for filename in section/*.wik
  do
  	echo !!! processing $filename ...
    pandoc $filename -f mediawiki -t latex --standalone -o ${filename%.*}.tex
    echo ... converted $filename to TeX.
  done
  
if [ "$(ls part/*.tex)" ]; then
  for filename in part/*.tex
    do
      echo !!! processing $filename ...
  	  title=$(sed -n '1p' $filename)
      sed -i '' -e '1,2d' $filename
      sed -i '' -e 's/\\end{document}//g;s/\\label.*}//g;s/\\\tightlist//g' $filename
      sed -i '' -e 's/\\section/\\part/g;s/\\subsection/\\section/g;s/\\subsubsection/\\subsection/g' $filename
	  python3 convert_tex_to_html.py > ${filename%.*}.html -f $filename -P -F -T "$title" | sed 's/ /\\ /g'
	  echo ... converted $filename to HTML.
    done
fi

if [ "$(ls section/*.tex)" ]; then  
  for filename in section/*.tex
    do
      echo !!! processing $filename ...
  	  title=$(sed -n '1p' $filename)
      sed -i '' -e '1,2d' $filename
      sed -i '' -e 's/\\end{document}//g;s/\\label.*}//g;s/\\\tightlist//g' $filename
      sed -i '' -e '1s/^/\\part{}\
/' $filename
	  python3 convert_tex_to_html.py > ${filename%.*}.html -f $filename -F -T "$title" | sed 's/ /\\ /g'
	  echo ... converted $filename to HTML.
    done
fi

mkdir -p final

echo !!! moving files ...

for filename in part/*.html
	do
	  mv $filename final/
	done
	
for filename in section/*.html
	do
	  mv $filename final/
	done
	
echo ... files 'in' final.