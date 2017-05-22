if [[ $# -eq 0 ]] ; then
    echo 'give CLA with file path! \n'
    exit 1
fi
echo "I hate kernel stuff" > $2
mv test.txt $1
echo "Written ' I hate kernel stuff' to $1 \n"

echo "reading file.. \n"
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"
done < "$2"
