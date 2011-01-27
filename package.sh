if [ $# -ne 1 ]
then
  echo "Usage: `basename $0` VERSION_NUMBER"
  exit 1
fi

ZIPNAME="MineSeeder X $1.zip"

rm "$ZIPNAME"
mkdir package
cp LICENSE package/
cp -R 'build/Release/MineSeeder X.app' package/
cd package
zip -r "$ZIPNAME" LICENSE 'MineSeeder X.app'
cp "$ZIPNAME" ../
cd ..
rm -rf package

echo ""
echo "DSA Signature"
echo "----------------------------------------"
sign_update.rb MineSeeder\ X\ 1.0.2.zip ~/Code/Support/Sparkle/dsa_priv.pem

LENGTH=`ruby -e 'puts \`du -c -k "build/Release/MineSeeder X.app"\`.split("\n").last.split("\t")[0]'`
echo ""
echo "Length: $LENGTH"
