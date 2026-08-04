package net.minecraft.client.renderer.texture;

import java.io.Closeable;
import java.io.IOException;

import net.lax1dude.eaglercraft.IOUtils;
import net.lax1dude.eaglercraft.opengl.ImageData;
import net.minecraft.client.resources.IResource;
import net.minecraft.client.resources.IResourceManager;
import net.minecraft.client.resources.data.TextureMetadataSection;
import net.minecraft.util.ResourceLocation;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import net.lax1dude.eaglercraft.EagRuntime;

public class SimpleTexture extends AbstractTexture {
	private static final Logger LOG = LogManager.getLogger();
	protected final ResourceLocation textureLocation;

	public SimpleTexture(ResourceLocation textureResourceLocation) {
		this.textureLocation = textureResourceLocation;
	}

	public void loadTexture(IResourceManager resourceManager) throws IOException {
		this.deleteGlTexture();
		IResource iresource = null;

		try {
			iresource = resourceManager.getResource(this.textureLocation);
			ImageData bufferedimage = null;
			try {
				bufferedimage = TextureUtil.readBufferedImage(iresource.getInputStream());
			}catch(IOException ex) {
				LOGGER.warn("Failed to read image for texture {}", this.textureLocation, ex);
				try {
					EagRuntime.debugPrintStackTraceToSTDERR(ex);
				}catch(Throwable t) {
					// ignore
				}
				throw ex;
			}
			boolean flag = false;
			boolean flag1 = false;

			if (iresource.hasMetadata()) {
				try {
					TextureMetadataSection texturemetadatasection = (TextureMetadataSection) iresource
							.getMetadata("texture");

					if (texturemetadatasection != null) {
						flag = texturemetadatasection.getTextureBlur();
						flag1 = texturemetadatasection.getTextureClamp();
					}
				} catch (RuntimeException runtimeexception) {
					LOG.warn("Failed reading metadata of: {}", this.textureLocation, runtimeexception);
				}
			}

			regenerateIfNotAllocated();
			TextureUtil.uploadTextureImageAllocate(this.getGlTextureId(), bufferedimage, flag, flag1);
		} finally {
			IOUtils.closeQuietly((Closeable) iresource);
		}
	}
}