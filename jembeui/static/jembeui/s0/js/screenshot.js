const juiCanTakeScreenshot  = navigator.mediaDevices.getDisplayMedia 

const juiTakeScreenshot = async () => {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: { mediaSource: 'screen' },
      })
      // get correct video track
      const track = stream.getVideoTracks()[0]
      // init Image Capture and not Video stream
      const imageCapture = new ImageCapture(track)
      // take first frame only
      const bitmap = await imageCapture.grabFrame()
      // destory video track to prevent more recording / mem leak
      track.stop()

      const canvas = document.createElement('canvas') 
      // this could be a document.createElement('canvas') if you want
      // draw weird image type to canvas so we can get a useful image
      canvas.width = bitmap.width
      canvas.height = bitmap.height
      const context = canvas.getContext('2d')
      context.drawImage(bitmap, 0, 0, bitmap.width, bitmap.height)
      const image = canvas.toDataURL()

      // this turns the base 64 string to a [File] object
      const res = await fetch(image)
      const buff = await res.arrayBuffer()
      // clone so we can rename, and put into array for easy proccessing
      const file = [
        new File([buff], `photo_${new Date()}.jpg`, {
          type: 'image/jpeg',
        }),
      ]
      return file 
}     


