dl_song() {
	local songs="${1}";
	local i="0";
	for song in ${songs};
	do
		printf "${i}. ${song}\n" | sed -e 's|/songs/||g' -e's|.html||g'
		i=$((i+1))
	done
}

search="Tum+hi+ho"
#albums=$(curl https://pagalnew.com/search.php\?find\=${search} | pup 'a[href*=album]' | grep href | cut -d'"' -f 2 | uniq)
songs=$(curl "https://pagalnew.com/search.php?find=${search}" | pup 'a[href*=songs]' | grep href | grep -v 'class="navbar"' | cut -d'"' -f2 | uniq)

#echo $albums
#echo $songs
dl_song "${songs}"
# Clean up some duplicates
# for a in $albums;
# do
# echo $a
# done
