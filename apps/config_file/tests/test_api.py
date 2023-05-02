from apps.action.tests.factories import ActionFactory
from apps.base.utils import CustomGraphQLTestCase


class ConfigFileTestCase(CustomGraphQLTestCase):
    def test_update_config_file(self):
        action = ActionFactory()
        response = self.query(
            """
            mutation updateConfigFile(
                $id: String!,
                $custom: Boolean!,
                $lossless: Boolean!,
                $lossy: Boolean!,
                $resize_type: String,
                $resize_percentage: Decimal,
                $resize_width: Int,
                $resize_height: Int,
                $resize_fit: String,
                $rename_prefix: String,
                $rename_suffix: String,
                $keep_exif: Boolean,
                $fix_orientation: Boolean,
                $image_quality: Decimal,
                $compression_filter: String,
                $keep_size: Boolean,
                $device_type: String,
                $maximum_file_size: Int,
                $convert_type: String,
                $full_optimized_web_package: Boolean) {
                updateConfigFile(
                    id: $id,
                    custom: $custom,
                    lossless: $lossless,
                    lossy: $lossy,
                    resizeType: $resize_type,
                    resizePercentage: $resize_percentage,
                    resizeWidth: $resize_width,
                    resizeHeight: $resize_height,
                    resizeFit: $resize_fit,
                    renamePrefix: $rename_prefix,
                    renameSuffix: $rename_suffix,
                    keepExif: $keep_exif,
                    fixOrientation: $fix_orientation,
                    imageQuality: $image_quality,
                    compressionFilter: $compression_filter,
                    keepSize: $keep_size,
                    deviceType: $device_type,
                    maximumFileSize: $maximum_file_size,
                    convertType: $convert_type,
                    fullOptimizedWebPackage: $full_optimized_web_package) {
                    verificationMessage
                }
            }
            """,
            variables={
                "id": str(action.config_file.id),
                "custom": True,
                "lossless": False,
                "lossy": True,
                "resize_type": "fit",
                "resize_percentage": 0.5,
                "resize_width": 800,
                "resize_height": 600,
                "resize_fit": "contain",
                "rename_prefix": "prefix",
                "rename_suffix": "suffix",
                "keep_exif": True,
                "fix_orientation": False,
                "image_quality": 0.8,
                "compression_filter": "webp",
                "keep_size": False,
                "device_type": "mobile",
                "maximum_file_size": 1024,
                "convert_type": "png",
                "full_optimized_web_package": True,
            },
        )
        print(response.json())
        self.assertEqual(
            response.json()["data"]["updateConfigFile"]["verificationMessage"],
            "Your config file has been updated.",
        )
