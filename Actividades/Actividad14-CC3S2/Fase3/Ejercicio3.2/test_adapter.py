from adapter import MockBucketAdapter


def test_adapter_simple_shape():
    null_block = {
        "resource": {
            "null_resource": {
                "myapp": {"triggers": {"k": "v"}}
            }
        }
    }
    adapter = MockBucketAdapter(null_block)
    out = adapter.to_bucket()
    assert "resource" in out
    assert "mock_cloud_bucket" in out["resource"]
    assert "myapp" in out["resource"]["mock_cloud_bucket"]
    assert out["resource"]["mock_cloud_bucket"]["myapp"]["name"] == "myapp"
    assert out["resource"]["mock_cloud_bucket"]["myapp"]["k"] == "v"


def test_adapter_list_shape():
    # Simulate the list-shaped factory output used in earlier exercises
    null_block = {
        "resource": [
            {
                "null_resource": [
                    {"appname": [{"triggers": {"a": 1}}]}
                ]
            }
        ]
    }
    adapter = MockBucketAdapter(null_block)
    out = adapter.to_bucket()
    assert "appname" in out["resource"]["mock_cloud_bucket"]
    assert out["resource"]["mock_cloud_bucket"]["appname"]["a"] == 1


if __name__ == "__main__":
    test_adapter_simple_shape()
    test_adapter_list_shape()
    print("adapter tests passed")
