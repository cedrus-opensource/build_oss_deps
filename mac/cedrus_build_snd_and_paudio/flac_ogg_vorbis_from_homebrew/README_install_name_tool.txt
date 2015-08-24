if you copy and paste the next line into a mac terminal:

find . -iname *dylib -exec otool -L {} \;

(assuming you do so from the root of the 'flac_ogg_vorbis_from_homebrew' folder)

you should see output like the following.

the important part is that ALL DYLIBS MUST BE PROCESSED WITH install_name_tool SO THAT THEY ARE CONFIGURED TO INSTALL TO:

@executable_path/../Frameworks/

--------------------

./flac/1.3.1/lib/libFLAC.8.dylib:
	@executable_path/../Frameworks/libFLAC.8.dylib (compatibility version 12.0.0, current version 12.0.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 169.3.0)
./libogg/1.3.2/lib/libogg.0.dylib:
	@executable_path/../Frameworks/libogg.0.dylib (compatibility version 9.0.0, current version 9.2.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 169.3.0)
./libvorbis/1.3.5/lib/libvorbis.0.dylib:
	@executable_path/../Frameworks/libvorbis.0.dylib (compatibility version 5.0.0, current version 5.8.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 169.3.0)
	@executable_path/../Frameworks/libogg.0.dylib (compatibility version 9.0.0, current version 9.2.0)
./libvorbis/1.3.5/lib/libvorbisenc.2.dylib:
	@executable_path/../Frameworks/libvorbisenc.2.dylib (compatibility version 3.0.0, current version 3.11.0)
	@executable_path/../Frameworks/libvorbis.0.dylib (compatibility version 5.0.0, current version 5.8.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 169.3.0)
	@executable_path/../Frameworks/libogg.0.dylib (compatibility version 9.0.0, current version 9.2.0)
./libvorbis/1.3.5/lib/libvorbisfile.3.dylib:
	@executable_path/../Frameworks/libvorbisfile.3.dylib (compatibility version 7.0.0, current version 7.7.0)
	@executable_path/../Frameworks/libvorbis.0.dylib (compatibility version 5.0.0, current version 5.8.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 169.3.0)
	@executable_path/../Frameworks/libogg.0.dylib (compatibility version 9.0.0, current version 9.2.0)