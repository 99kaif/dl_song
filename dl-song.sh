err() {
	echo $1
	exit
}

help() {
	echo "USES: dl-song.sh <argument> <song/album/movie name>"
	echo "arguments:"
	echo -e "\t-s or --song: to download a song"
	echo -e "\t-a or --album: to download all songs of a movie"
}

dl_song() {
	local song_urls="${1}";
	local song_names=();
	local i="0";
	for song in ${song_urls};
	do
		name=$(printf "${song}\n" | sed -e 's|/songs/||g' -e's|.html||g')
		echo "${i}." $name
		song_names+=("$name")
		i=$((i+1))
	done
	if [ $i == "0" ]; then
		err "no song found"
	fi
	local song_urls=(${song_urls}) # Spliting the 'song_urls' string to array by space
	echo -n "Enter a song: "
	if read -r input;
	then
		echo "You have selected"  "\"$(printf "${song_urls[${input}]}\n" | sed -e 's|/songs/||g' -e's|.html||g')\"" 
	else
		echo "Coudn't read the input"
		return
	fi
	dlink="https://pagalnew.com"$(curl "https://pagalnew.com${song_urls[${input}]}" | grep '<a.*class="dbutton".*320 KBPS.*' | cut -d'"' -f8)
	echo $dlink
	echo ${song_names[${input}]}
	curl $dlink --output "${song_names[${input}]}" --http1.1
}

dl_album() {
	local album_urls="${1}";
	local album_names=();
	local i="0";
	for song in ${album_urls};
	do
		name=$(printf "${song}\n" | sed -e 's|/album/||g' -e's|.html||g')
		echo "${i}." $name
		album_names+=("$name")
		i=$((i+1))
	done
	if [ $i == "0" ]; then
		err "no song found"
	fi
	local album_urls=(${album_urls}) # Spliting the 'album_urls' string to array by space
	echo -n "Enter a album number: "
	if read -r input;
	then
		echo "You have selected"  "\"$(printf "${album_urls[${input}]}\n" | sed -e 's|/album/||g' -e's|.html||g')\"" 
	else
		echo "Coudn't read the input"
		return
	fi
	echo ${album_urls[${input}]}
	songs=($(curl "https://pagalnew.com${album_urls[${input}]}" | grep '.*<a.*href.*songs.*' | grep -v '.*class="navbar"' | grep -ohE 'https://pagalnew.com/songs/[^">]*'))
	#echo ${songs[@]}
	for song in ${songs[@]};
	do
		name=$(printf "${song}\n" | sed -e 's|.*/songs/||g' -e's|.html||g')
		echo $name
		dlink="https://pagalnew.com"$(curl "${song}" | grep '<a.*class="dbutton".*320 KBPS.*' | cut -d'"' -f8)
		curl ${dlink} --output "${name}" --http1.1
	done
}

init() {
	local Type="${1}"
	shift
	local search="${@}"
	echo  "${search}" | grep -n '[^a-zA-Z0-9 ]' && err 'you can only enter alphanumeric characters'
	local search="$(echo -n "${search}" | sed -E 's/\s+/%20/g')"
	echo $search
	if [ "${Type}" == "--song" -o "${Type}" == "-s" ]; then
		local songs=$(curl "https://pagalnew.com/search.php?find=${search}" | grep '<a.*href.*=.*songs' | grep href | grep -v 'class="navbar"' | cut -d'"' -f2 | uniq)
		dl_song "${songs}"
	elif [ "${Type}" == "--album" -o "${Type}" == "-a" ]; then
		albums=$(curl https://pagalnew.com/search.php\?find\=${search} | grep '<a.*href.*=.*album' | grep href | cut -d'"' -f 2 | uniq)
		dl_album "${albums}"
	else
		help
		err "invalid argument"
	fi
}

init $@
