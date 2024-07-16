import { Canvas, loadImage } from 'skia-canvas'
import path from 'path'
import fs from 'fs'

async function resize (imagePath: string) {
  const image = await loadImage(imagePath)

  const canvas = new Canvas(Math.max(image.width, image.height), Math.max(image.width, image.height))
  const ctx = canvas.getContext('2d')

  ctx.drawImage(
    image,

    (canvas.width / 2) - (image.width / 2),
    (canvas.height / 2) - (image.height / 2),

    image.width,
    image.height
  )

  fs.writeFileSync(imagePath, await canvas.toBuffer('png'))
}

resize(path.join(__dirname, 'asset', 'image', 'explosion_1.png'))
resize(path.join(__dirname, 'asset', 'image', 'explosion_2.png'))
resize(path.join(__dirname, 'asset', 'image', 'explosion_3.png'))
resize(path.join(__dirname, 'asset', 'image', 'explosion_4.png'))
resize(path.join(__dirname, 'asset', 'image', 'explosion_5.png'))
resize(path.join(__dirname, 'asset', 'image', 'explosion_6.png'))
resize(path.join(__dirname, 'asset', 'image', 'explosion_7.png'))
